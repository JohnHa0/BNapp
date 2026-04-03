// 隐藏 Windows 的控制台窗口（仅在 release 模式下生效）
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use tauri::Manager;
use tauri_plugin_shell::ShellExt;
use tauri_plugin_shell::process::CommandChild;
use tauri_plugin_log::{Builder, Target, TargetKind};
use std::sync::Mutex;

// 保存 Sidecar 子进程句柄，以便在应用退出时正确终止后端
struct SidecarChild(Mutex<Option<CommandChild>>);

/// 强制杀掉占用指定端口的进程（Windows 专用后备方案）
#[cfg(target_os = "windows")]
fn force_kill_port(port: u16) {
    use std::process::Command;
    // 查找占用端口的 PID
    let output = Command::new("cmd")
        .args(["/C", &format!("netstat -ano | findstr :{} | findstr LISTENING", port)])
        .output();

    if let Ok(output) = output {
        let stdout = String::from_utf8_lossy(&output.stdout);
        for line in stdout.lines() {
            if let Some(pid_str) = line.split_whitespace().last() {
                if let Ok(pid) = pid_str.parse::<u32>() {
                    if pid > 0 {
                        log::info!("强制终止占用端口 {} 的进程 PID={}", port, pid);
                        let _ = Command::new("taskkill")
                            .args(["/F", "/PID", &pid.to_string()])
                            .output();
                    }
                }
            }
        }
    }
}

#[cfg(not(target_os = "windows"))]
fn force_kill_port(_port: u16) {
    // macOS/Linux: 暂不实现
}

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

      let (mut rx, child) = sidecar_command
        .spawn()
        .expect("Failed to spawn sidecar. Ensure main.exe exists in binaries folder.");

      // 将子进程句柄存入 Tauri 状态管理器，应用退出时可获取并终止
      app.manage(SidecarChild(Mutex::new(Some(child))));

      // 实时捕获后端输出并写入本地日志文件
      tauri::async_runtime::spawn(async move {
        while let Some(event) = rx.recv().await {
          match event {
            tauri_plugin_shell::process::CommandEvent::Stdout(line) => {
              log::info!("[Backend] {}", String::from_utf8_lossy(&line).trim());
            }
            tauri_plugin_shell::process::CommandEvent::Stderr(line) => {
              let msg = String::from_utf8_lossy(&line);
              let trimmed = msg.trim();
              // 智能识别 Python 日志级别，避免所有 stderr 输出都标为 ERROR
              if trimmed.contains("[ERROR]") || trimmed.contains("Traceback") || trimmed.contains("Error") {
                log::error!("[Backend] {}", trimmed);
              } else if trimmed.contains("[WARNING]") || trimmed.contains("WARNING") {
                log::warn!("[Backend] {}", trimmed);
              } else {
                log::info!("[Backend] {}", trimmed);
              }
            }
            _ => {}
          }
        }
      });

      Ok(())
    })
    .on_window_event(|window, event| {
      // 窗口关闭时：1. 先终止 Sidecar 子进程  2. 再强制清理端口 (双保险)
      if let tauri::WindowEvent::Destroyed = event {
        // 第一步：终止 Sidecar 子进程句柄
        let state = window.state::<SidecarChild>();
        if let Ok(mut guard) = state.0.lock() {
          if let Some(child) = guard.take() {
            log::info!("正在终止后端 Sidecar 进程...");
            let _ = child.kill();
            log::info!("后端 Sidecar 进程已发送终止信号");
          }
        }
        // 第二步：强制清理端口，防止进程未响应 kill 信号
        force_kill_port(18521);
        log::info!("端口清理完成，应用安全退出");
      }
    })
    .run(tauri::generate_context!())
    .expect("error while running tauri application");
}
