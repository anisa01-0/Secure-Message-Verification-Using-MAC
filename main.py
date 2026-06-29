import customtkinter as ctk
from mac_utils import generate_mac, verify_mac

# =============== CONFIGURATION ===============
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# =============== MAIN APPLICATION ===============
app = ctk.CTk()
app.title("Secure Message Verification Using MAC")
app.geometry("1000x650")
app.minsize(900, 550)

# Configure grid
app.grid_columnconfigure(0, weight=1)
app.grid_columnconfigure(1, weight=1)
app.grid_rowconfigure(0, weight=1)

# =============== HEADER ===============
header = ctk.CTkFrame(app, height=60, corner_radius=0, fg_color=("#1a1a2e", "#16213e"))
header.grid(row=0, column=0, columnspan=2, sticky="ew", padx=0, pady=0)
header.grid_propagate(False)

ctk.CTkLabel(
    header, 
    text="🔐 Secure Message Verification System", 
    font=("Segoe UI", 28, "bold"),
    text_color="#00d4ff"
).pack(pady=10)

# =============== SENDER FRAME ===============
sender_frame = ctk.CTkFrame(
    app, 
    corner_radius=20,
    border_width=2,
    border_color="#00d4ff"
)
sender_frame.grid(row=1, column=0, padx=25, pady=20, sticky="nsew")

# Sender Header
ctk.CTkLabel(
    sender_frame, 
    text="📤 SENDER", 
    font=("Segoe UI", 22, "bold"),
    text_color="#00d4ff"
).pack(pady=(15, 10))

ctk.CTkLabel(
    sender_frame, 
    text="Enter the message and secret key to generate MAC", 
    font=("Segoe UI", 12),
    text_color="gray"
).pack(pady=(0, 15))

# ===== Message Input with Placeholder =====
ctk.CTkLabel(sender_frame, text="📝 Message", font=("Segoe UI", 14, "bold"), anchor="w").pack(fill="x", padx=25, pady=(10, 0))

message_input = ctk.CTkTextbox(sender_frame, width=380, height=100, corner_radius=12, border_width=1)
message_input.pack(pady=5, padx=25)

# Placeholder for Message
MESSAGE_PLACEHOLDER = "Enter your secret message here..."
message_input.insert("1.0", MESSAGE_PLACEHOLDER)
message_input._placeholder_active = True  # Custom attribute to track state

def on_message_focus_in(event):
    """Remove placeholder when user clicks on textbox"""
    if message_input.get("1.0", "end-1c").strip() == MESSAGE_PLACEHOLDER:
        message_input.delete("1.0", "end")
        message_input._placeholder_active = False

def on_message_focus_out(event):
    """Restore placeholder if textbox is empty"""
    if message_input.get("1.0", "end-1c").strip() == "":
        message_input.insert("1.0", MESSAGE_PLACEHOLDER)
        message_input._placeholder_active = True

message_input.bind("<FocusIn>", on_message_focus_in)
message_input.bind("<FocusOut>", on_message_focus_out)

# ===== Secret Key Input =====
ctk.CTkLabel(sender_frame, text="🔑 Secret Key", font=("Segoe UI", 14, "bold"), anchor="w").pack(fill="x", padx=25, pady=(15, 0))

key_input = ctk.CTkEntry(
    sender_frame, 
    width=380, 
    placeholder_text="Enter shared secret key...", 
    show="*",
    corner_radius=12,
    border_width=1
)
key_input.pack(pady=5, padx=25)

# ===== MAC Output =====
ctk.CTkLabel(sender_frame, text="🔐 Generated MAC", font=("Segoe UI", 14, "bold"), anchor="w").pack(fill="x", padx=25, pady=(15, 0))

mac_output = ctk.CTkTextbox(
    sender_frame, 
    width=380, 
    height=70, 
    corner_radius=12, 
    border_width=1,
    fg_color=("#1e1e2e", "#2d2d44")
)
mac_output.pack(pady=5, padx=25)
mac_output.insert("1.0", "Click 'Generate MAC' to create...")
mac_output.configure(state="disabled")

# ===== Generate Button Function =====
def generate_mac_action():
    msg = message_input.get("1.0", "end-1c").strip()
    key = key_input.get().strip()
    
    # Check if message is placeholder or empty
    if msg == MESSAGE_PLACEHOLDER or msg == "":
        mac_output.configure(state="normal")
        mac_output.delete("1.0", "end")
        mac_output.insert("1.0", "⚠️ Please enter a message!")
        mac_output.configure(state="disabled")
        return
    
    if not key:
        mac_output.configure(state="normal")
        mac_output.delete("1.0", "end")
        mac_output.insert("1.0", "⚠️ Please enter a secret key!")
        mac_output.configure(state="disabled")
        return
    
    mac = generate_mac(msg, key)
    mac_output.configure(state="normal")
    mac_output.delete("1.0", "end")
    mac_output.insert("1.0", mac)
    mac_output.configure(state="disabled")

generate_btn = ctk.CTkButton(
    sender_frame, 
    text="🚀 Generate MAC", 
    width=380, 
    height=45,
    corner_radius=12,
    font=("Segoe UI", 16, "bold"),
    fg_color="#00d4ff",
    hover_color="#0099cc",
    command=generate_mac_action
)
generate_btn.pack(pady=(15, 10))

# =============== RECEIVER FRAME ===============
receiver_frame = ctk.CTkFrame(
    app, 
    corner_radius=20,
    border_width=2,
    border_color="#ff6b6b"
)
receiver_frame.grid(row=1, column=1, padx=25, pady=20, sticky="nsew")

# Receiver Header
ctk.CTkLabel(
    receiver_frame, 
    text="📥 RECEIVER", 
    font=("Segoe UI", 22, "bold"),
    text_color="#ff6b6b"
).pack(pady=(15, 10))

ctk.CTkLabel(
    receiver_frame, 
    text="Enter received data and verify MAC", 
    font=("Segoe UI", 12),
    text_color="gray"
).pack(pady=(0, 15))

# ===== Received Message with Placeholder =====
ctk.CTkLabel(receiver_frame, text="📝 Received Message", font=("Segoe UI", 14, "bold"), anchor="w").pack(fill="x", padx=25, pady=(10, 0))

received_msg_input = ctk.CTkTextbox(receiver_frame, width=380, height=100, corner_radius=12, border_width=1)
received_msg_input.pack(pady=5, padx=25)

# Placeholder for Received Message
RECEIVED_MSG_PLACEHOLDER = "Paste received message here..."
received_msg_input.insert("1.0", RECEIVED_MSG_PLACEHOLDER)
received_msg_input._placeholder_active = True

def on_received_msg_focus_in(event):
    if received_msg_input.get("1.0", "end-1c").strip() == RECEIVED_MSG_PLACEHOLDER:
        received_msg_input.delete("1.0", "end")
        received_msg_input._placeholder_active = False

def on_received_msg_focus_out(event):
    if received_msg_input.get("1.0", "end-1c").strip() == "":
        received_msg_input.insert("1.0", RECEIVED_MSG_PLACEHOLDER)
        received_msg_input._placeholder_active = True

received_msg_input.bind("<FocusIn>", on_received_msg_focus_in)
received_msg_input.bind("<FocusOut>", on_received_msg_focus_out)

# ===== Received Secret Key =====
ctk.CTkLabel(receiver_frame, text="🔑 Secret Key", font=("Segoe UI", 14, "bold"), anchor="w").pack(fill="x", padx=25, pady=(15, 0))

received_key_input = ctk.CTkEntry(
    receiver_frame, 
    width=380, 
    placeholder_text="Enter shared secret key...", 
    show="*",
    corner_radius=12,
    border_width=1
)
received_key_input.pack(pady=5, padx=25)

# ===== Received MAC with Placeholder =====
ctk.CTkLabel(receiver_frame, text="🔐 Received MAC", font=("Segoe UI", 14, "bold"), anchor="w").pack(fill="x", padx=25, pady=(15, 0))

received_mac_input = ctk.CTkTextbox(
    receiver_frame, 
    width=380, 
    height=70, 
    corner_radius=12, 
    border_width=1
)
received_mac_input.pack(pady=5, padx=25)

# Placeholder for Received MAC
RECEIVED_MAC_PLACEHOLDER = "Paste received MAC here..."
received_mac_input.insert("1.0", RECEIVED_MAC_PLACEHOLDER)
received_mac_input._placeholder_active = True

def on_received_mac_focus_in(event):
    if received_mac_input.get("1.0", "end-1c").strip() == RECEIVED_MAC_PLACEHOLDER:
        received_mac_input.delete("1.0", "end")
        received_mac_input._placeholder_active = False

def on_received_mac_focus_out(event):
    if received_mac_input.get("1.0", "end-1c").strip() == "":
        received_mac_input.insert("1.0", RECEIVED_MAC_PLACEHOLDER)
        received_mac_input._placeholder_active = True

received_mac_input.bind("<FocusIn>", on_received_mac_focus_in)
received_mac_input.bind("<FocusOut>", on_received_mac_focus_out)

# ===== Result Label =====
result_label = ctk.CTkLabel(
    receiver_frame, 
    text="", 
    font=("Segoe UI", 20, "bold")
)
result_label.pack(pady=(10, 5))

# ===== Verify Button Function =====
def verify_message_action():
    msg = received_msg_input.get("1.0", "end-1c").strip()
    key = received_key_input.get().strip()
    mac = received_mac_input.get("1.0", "end-1c").strip()
    
    # Check for placeholders
    if msg == RECEIVED_MSG_PLACEHOLDER or msg == "":
        result_label.configure(text="⚠️ Please paste a message!", text_color="#ffd93d")
        return
    
    if not key:
        result_label.configure(text="⚠️ Please enter a secret key!", text_color="#ffd93d")
        return
    
    if mac == RECEIVED_MAC_PLACEHOLDER or mac == "":
        result_label.configure(text="⚠️ Please paste a MAC!", text_color="#ffd93d")
        return
    
    if verify_mac(msg, key, mac):
        result_label.configure(text="✅ MESSAGE IS VALID", text_color="#6bcb77")
    else:
        result_label.configure(text="❌ MESSAGE WAS CHANGED", text_color="#ff6b6b")

verify_btn = ctk.CTkButton(
    receiver_frame, 
    text="🔍 Verify Message", 
    width=380, 
    height=45,
    corner_radius=12,
    font=("Segoe UI", 16, "bold"),
    fg_color="#ff6b6b",
    hover_color="#cc5555",
    command=verify_message_action
)
verify_btn.pack(pady=(15, 10))

# =============== FOOTER ===============
footer = ctk.CTkFrame(app, height=40, corner_radius=0, fg_color=("#1a1a2e", "#16213e"))
footer.grid(row=2, column=0, columnspan=2, sticky="ew", padx=0, pady=0)
footer.grid_propagate(False)

ctk.CTkLabel(
    footer, 
    text="🔒 Integrity & Authentication | HMAC-SHA256 | Secure Message Verification", 
    font=("Segoe UI", 12),
    text_color="#888899"
).pack(pady=10)

# =============== RUN APPLICATION ===============
if __name__ == "__main__":
    app.mainloop()