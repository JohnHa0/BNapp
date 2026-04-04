use std::env;
use std::fs;
use std::path::{Path, PathBuf};

fn main() {
    // 1. Determine the build target directory (e.g., target/debug or target/release)
    // OUT_DIR is usually something like target/debug/build/hb-eval-system-hash/out
    if let Ok(out_dir_str) = env::var("OUT_DIR") {
        let out_dir = PathBuf::from(out_dir_str);
        // Navigate up 3 levels to reach the profile directory (debug/release)
        if let Some(target_dir) = out_dir.parent().and_then(|p| p.parent()).and_then(|p| p.parent()) {
            
            // 2. Source path: src-tauri/binaries/_internal
            let manifest_dir = PathBuf::from(env::var("CARGO_MANIFEST_DIR").unwrap());
            let src_internal = manifest_dir.join("binaries").join("_internal");
            
            // 3. Destination path: target/debug/_internal
            let dest_internal = target_dir.join("_internal");

            // 4. Sync the _internal directory if it exists
            if src_internal.exists() {
                // Tell Cargo to rerun this script if the source changes
                println!("cargo:rerun-if-changed={}", src_internal.display());
                
                if let Err(e) = copy_dir_all(&src_internal, &dest_internal) {
                    println!("cargo:warning=Failed to sync _internal folder: {}", e);
                } else {
                    println!("cargo:info=Synced _internal to {}", dest_internal.display());
                }
            }
        }
    }

    tauri_build::build()
}

/// Helper function to copy a directory recursively
fn copy_dir_all(src: &Path, dst: &Path) -> std::io::Result<()> {
    if !dst.exists() {
        fs::create_dir_all(dst)?;
    }
    for entry in fs::read_dir(src)? {
        let entry = entry?;
        let ty = entry.file_type()?;
        if ty.is_dir() {
            copy_dir_all(&entry.path(), &dst.join(entry.file_name()))?;
        } else {
            fs::copy(entry.path(), &dst.join(entry.file_name()))?;
        }
    }
    Ok(())
}
