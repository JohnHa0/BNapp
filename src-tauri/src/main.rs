use tauri_plugin_shell::ShellExt;
use tauri_plugin_log::{Builder, Target, TargetKind};

fn main() {
  tauri::Builder::default()
    .plugin(tauri_plugin_dialog::init())
    .plugin(tauri_plugin_fs::init())
    .plugin(tauri_plugin_shell::init())
    .plugin(
        Builder::new()
            .target(Target::new(TargetKind::Stdout))
            .target(Target::new(TargetKind::LogDir { 
                file_name: Some("app.log".to_string()) 
            }))
            .level(log::LevelFilter::Info)
            .build()
    )
    .setup(|app| {
      // 自动拉起 Python 后端 Sidecar
      let shell = app.shell();
      let sidecar_command = shell
        .sidecar("main")
        .expect("Failed to create sidecar command. Check tauri.conf.json identifier.");

      let (mut rx, _child) = sidecar_command
        .spawn()
        .expect("Failed to spawn sidecar. Ensure main.exe exists in binaries folder.");

      // 实时捕获后端输出并写入本地日志文件
      tauri::async_runtime::spawn(async move {
        while let Some(event) = rx.recv().await {
          match event {
            tauri_plugin_shell::process::CommandEvent::Stdout(line) => {
              log::info!("[Backend] {}", String::from_utf8_lossy(&line).trim());
            }
            tauri_plugin_shell::process::CommandEvent::Stderr(line) => {
              log::error!("[Backend Error] {}", String::from_utf8_lossy(&line).trim());
            }
            _ => {}
          }
        }
      });

      Ok(())
    })
    .run(tauri::generate_context!())
    .expect("error while running tauri application");
}
