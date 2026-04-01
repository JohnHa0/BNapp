// Prevents additional console window on Windows in release, DO NOT REMOVE!!
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

fn main() {
  tauri::Builder::default()
    .plugin(tauri_plugin_shell::init())
    .setup(|_app| {
      // Sidecar (Python process) should be launched here or from the frontend
      // through the shell plugin using the "main" identifier.
      Ok(())
    })
    .run(tauri::generate_context!())
    .expect("error while running tauri application");
}
