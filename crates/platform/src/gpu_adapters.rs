//! Windows DXGI adapter names for honest GPU encoding diagnostics.
//! Detecting a GPU vendor is NOT proof that AMF/QSV/NVENC encoding works.
//! Discovery runs off the egui paint thread and never creates an encoder.
use std::sync::{Once, OnceLock};
use windows::Win32::Graphics::Dxgi::{CreateDXGIFactory1, IDXGIFactory1};

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum Vendor { Nvidia, Amd, Intel, Other }

impl Vendor {
    pub fn from_pci_id(id: u32) -> Self {
        match id { 0x10de => Self::Nvidia, 0x1002 | 0x1022 => Self::Amd, 0x8086 => Self::Intel, _ => Self::Other }
    }
    pub fn label(self) -> &'static str {
        match self { Self::Nvidia => "NVIDIA", Self::Amd => "AMD", Self::Intel => "Intel", Self::Other => "Other" }
    }
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Adapter { pub vendor: Vendor, pub name: String }

static ADAPTERS: OnceLock<Vec<Adapter>> = OnceLock::new();
static H264_MFT_ENCODERS: OnceLock<Result<Vec<String>, String>> = OnceLock::new();

fn enumerate() -> Vec<Adapter> {
    // SAFETY: DXGI COM factory owns the enumerated adapter references; GetDesc1
    // returns an owned POD description. No pointers escape this block.
    unsafe {
        let factory: IDXGIFactory1 = match CreateDXGIFactory1() {
            Ok(f) => f,
            Err(e) => { log::info!("GPU adapter inspection unavailable: {e}"); return Vec::new(); }
        };
        let mut out = Vec::new();
        for i in 0..16u32 {
            let Ok(adapter) = factory.EnumAdapters1(i) else { break };
            let Ok(desc) = adapter.GetDesc1() else { continue };
            // Microsoft's Basic Render Driver is software, not a physical GPU.
            if desc.VendorId == 0x1414 { continue; }
            let len = desc.Description.iter().position(|&ch| ch == 0).unwrap_or(desc.Description.len());
            let name = String::from_utf16_lossy(&desc.Description[..len]);
            out.push(Adapter { vendor: Vendor::from_pci_id(desc.VendorId), name });
        }
        out
    }
}

/// Initialize once on a worker. `result()` stays nonblocking on egui's UI thread.
pub fn warm_probe() {
    static STARTED: Once = Once::new();
    STARTED.call_once(|| {
        let launch = std::thread::Builder::new().name("filmcraft-dxgi-adapters".into()).spawn(|| {
            let _ = ADAPTERS.get_or_init(enumerate);
        });
        if let Err(e) = launch { log::info!("Could not launch GPU adapter probe: {e}"); }
    });
}

/// None while waiting; Some(empty) when no hardware adapter can be enumerated.
pub fn result() -> Option<Vec<Adapter>> { ADAPTERS.get().cloned() }

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn gpu_vendor_id_is_not_encoder_availability() {
        assert_eq!(Vendor::from_pci_id(0x1002), Vendor::Amd);
        assert_eq!(Vendor::from_pci_id(0x8086), Vendor::Intel);
        assert_eq!(Vendor::from_pci_id(0x10de), Vendor::Nvidia);
        assert_eq!(Vendor::from_pci_id(0x1234), Vendor::Other);
        assert_eq!(Vendor::Intel.label(), "Intel");
    }
}

/// Probe actual hardware-registered H.264 Media Foundation encoder transforms
/// asynchronously. Vendor identification alone does not count as a capability.
/// This discovery does not activate an encoder or register an export factory.
pub fn warm_h264_encoder_probe() {
    static STARTED: Once = Once::new();
    STARTED.call_once(|| {
        if let Err(e) = std::thread::Builder::new().name("filmcraft-mf-h264-encoders".into()).spawn(|| {
            let _ = H264_MFT_ENCODERS.get_or_init(crate::media_foundation::h264_hardware_encoder_candidates);
        }) {
            log::warn!("Could not start Media Foundation encoder discovery: {e}");
            let _ = H264_MFT_ENCODERS.set(Err(format!("Encoder discovery thread unavailable: {e}")));
        }
    });
}

/// None while probing; otherwise encoder names or a diagnostic error.
/// Safe to call while painting the egui UI (nonblocking).
pub fn h264_encoder_probe_result() -> Option<Result<Vec<String>, String>> {
    H264_MFT_ENCODERS.get().cloned()
}
