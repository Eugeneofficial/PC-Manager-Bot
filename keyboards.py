from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def get_main_keyboard():
    keyboard = [
        [
            InlineKeyboardButton("💻 System Control", callback_data='system_control'),
            InlineKeyboardButton("📊 System Info", callback_data='system_info')
        ],
        [
            InlineKeyboardButton("📂 Files", callback_data='files'),
            InlineKeyboardButton("⚙️ Processes", callback_data='processes')
        ],
        [
            InlineKeyboardButton("🔍 Search", callback_data='search'),
            InlineKeyboardButton("⚡ Quick Actions", callback_data='quick')
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_system_control_keyboard():
    keyboard = [
        [
            InlineKeyboardButton("🔄 Restart", callback_data='sys_restart'),
            InlineKeyboardButton("⭕ Shutdown", callback_data='sys_shutdown')
        ],
        [
            InlineKeyboardButton("🔒 Lock", callback_data='sys_lock'),
            InlineKeyboardButton("💤 Sleep", callback_data='sys_sleep')
        ],
        [
            InlineKeyboardButton("🔊 Volume +", callback_data='sys_vol_up'),
            InlineKeyboardButton("🔈 Volume -", callback_data='sys_vol_down')
        ],
        [InlineKeyboardButton("🔙 Back", callback_data='main_menu')]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_files_keyboard(current_path=None):
    keyboard = [
        [
            InlineKeyboardButton("📂 Browse", callback_data='files_browse'),
            InlineKeyboardButton("📤 Upload", callback_data='files_upload')
        ],
        [
            InlineKeyboardButton("📥 Download", callback_data='files_download'),
            InlineKeyboardButton("✂️ Cut/Copy/Paste", callback_data='files_clipboard')
        ],
        [InlineKeyboardButton("🔙 Back", callback_data='main_menu')]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_processes_keyboard():
    keyboard = [
        [
            InlineKeyboardButton("📊 View Processes", callback_data='proc_view'),
            InlineKeyboardButton("❌ Kill Process", callback_data='proc_kill')
        ],
        [
            InlineKeyboardButton("🔄 Refresh", callback_data='proc_refresh'),
            InlineKeyboardButton("📈 Performance", callback_data='proc_perf')
        ],
        [InlineKeyboardButton("🔙 Back", callback_data='main_menu')]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_search_keyboard():
    keyboard = [
        [
            InlineKeyboardButton("🔍 By Name", callback_data='search_name'),
            InlineKeyboardButton("📅 By Date", callback_data='search_date')
        ],
        [
            InlineKeyboardButton("📦 By Size", callback_data='search_size'),
            InlineKeyboardButton("📝 By Type", callback_data='search_type')
        ],
        [InlineKeyboardButton("🔙 Back", callback_data='main_menu')]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_quick_actions_keyboard():
    keyboard = [
        [
            InlineKeyboardButton("📸 Screenshot", callback_data='quick_screen'),
            InlineKeyboardButton("📋 Clipboard", callback_data='quick_clip')
        ],
        [
            InlineKeyboardButton("🎵 Media Control", callback_data='quick_media'),
            InlineKeyboardButton("🖥️ Monitor", callback_data='quick_monitor')
        ],
        [InlineKeyboardButton("🔙 Back", callback_data='main_menu')]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_file_browser_keyboard(items, current_path, page=0):
    keyboard = []
    
    # Add parent directory button if not in root
    if current_path and current_path != "/":
        keyboard.append([InlineKeyboardButton("📁 ..", callback_data='file_parent')])
    
    # Add files and directories
    start_idx = page * 8
    end_idx = start_idx + 8
    current_items = items[start_idx:end_idx]
    
    for item in current_items:
        name, is_dir = item
        icon = "📁" if is_dir else "📄"
        callback_data = f'{"dir" if is_dir else "file"}:{name}'
        keyboard.append([InlineKeyboardButton(f"{icon} {name}", callback_data=callback_data)])
    
    # Navigation row
    nav_row = []
    if page > 0:
        nav_row.append(InlineKeyboardButton("⬅️ Previous", callback_data='file_prev'))
    if end_idx < len(items):
        nav_row.append(InlineKeyboardButton("Next ➡️", callback_data='file_next'))
    if nav_row:
        keyboard.append(nav_row)
    
    # Control buttons
    keyboard.append([
        InlineKeyboardButton("📤 Upload", callback_data='file_upload'),
        InlineKeyboardButton("🔄 Refresh", callback_data='file_refresh')
    ])
    keyboard.append([InlineKeyboardButton("🔙 Back", callback_data='files')])
    
    return InlineKeyboardMarkup(keyboard)

def get_media_control_keyboard():
    keyboard = [
        [
            InlineKeyboardButton("⏮️ Previous", callback_data='media_prev'),
            InlineKeyboardButton("⏯️ Play/Pause", callback_data='media_play'),
            InlineKeyboardButton("⏭️ Next", callback_data='media_next')
        ],
        [
            InlineKeyboardButton("🔊 Volume +", callback_data='media_vol_up'),
            InlineKeyboardButton("🔈 Volume -", callback_data='media_vol_down'),
            InlineKeyboardButton("🔇 Mute", callback_data='media_mute')
        ],
        [InlineKeyboardButton("🔙 Back", callback_data='quick')]
    ]
    return InlineKeyboardMarkup(keyboard)
