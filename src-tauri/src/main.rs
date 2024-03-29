#![cfg_attr(
    all(not(debug_assertions), target_os = "windows"),
    windows_subsystem = "windows"
)]

use std::process::Command;
use std::sync::{Arc, Mutex};
use tauri::api::dialog;
use tauri::{Manager, State};

mod state;

struct AppState(Arc<Mutex<state::App>>);

#[tauri::command]
fn project_new(handle: tauri::AppHandle, app_state: State<AppState>) {
    println!("New project clicked.");
}

#[tauri::command]
fn project_open(handle: tauri::AppHandle, app_state: State<AppState>) {
    println!("Open project clicked.");
}

fn main() {
    tauri::Builder::default()
        .manage(AppState(Default::default()))
        .invoke_handler(tauri::generate_handler![
            project_new,
            project_open, 
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
