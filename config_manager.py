import customtkinter as ctk
import json
import os
import webbrowser
import sys

# Define o caminho do settings.json focando na pasta de usuário raiz
USER_HOME = os.path.expanduser("~")
BASE_DIR = os.path.join(USER_HOME, ".claude")

# Garante que o diretório .claude exista na pasta do usuário
os.makedirs(BASE_DIR, exist_ok=True)

SETTINGS_FILE = os.path.join(BASE_DIR, 'settings.json')

def save_settings(data):
    with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

def load_or_create_settings():
    if not os.path.exists(SETTINGS_FILE):
        default_data = {
            "env": {
                "CLAUDE_CODE_USE_OPENAI": "1",
                "OPENAI_BASE_URL": "https://openrouter.ai/api/v1",
                "OPENAI_MODEL": "",
                "OPENAI_API_KEY": ""
            }
        }
        save_settings(default_data)
        return default_data
    try:
        with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {"env": {}}

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.current_lang = "pt"
        
        # Dicionário I18n Internacionalização
        self.i18n = {
            "pt": {
                "window": "OpenClaude Models Manager",
                "header": "Configurações OpenClaude",
                "subtitle": "Gerencie seu acesso e modelos de IA",
                "model_lbl": "NOME DO MODELO",
                "key_lbl": "CHAVE DE API (OPENROUTER)",
                "btn_free": "Models Free",
                "btn_gen": "Gerar API Key",
                "check_vis": "Visível",
                "btn_save": "Salvar Modificações",
                "msg_save": "✔ Configurações registradas!",
                "lang_btn": "EN"
            },
            "en": {
                "window": "OpenClaude Studio",
                "header": "OpenClaude Settings",
                "subtitle": "Manage your AI models and API access",
                "model_lbl": "MODEL NAME",
                "key_lbl": "API KEY (OPENROUTER)",
                "btn_free": "Free Models",
                "btn_gen": "Generate Key",
                "check_vis": "Visible",
                "btn_save": "Save Changes",
                "msg_save": "✔ Settings successfully saved!",
                "lang_btn": "PTBR"
            }
        }
        
        # Tema Escuro Minimalista (OLED / Pitch Black)
        self.title("OpenClaude Studio")
        self.geometry("640x550")
        self.resizable(False, False)
        # Fundo ultradark
        self.configure(fg_color="#121212")
        
        ctk.set_appearance_mode("dark")
        
        # Fontes
        TITLE_FONT = ("Inter", 24, "bold")
        SUB_FONT = ("Inter", 12)
        LABEL_FONT = ("Inter", 11, "bold")
        MAIN_FONT = ("Inter", 14)
        ICON_FONT = ("Segoe UI Emoji", 16)
        
        # Botão de Bandeira Flutuante Topo-Esquerdo
        self.btn_lang = ctk.CTkButton(self, text="", font=("Inter", 12, "bold"), width=70, height=30,
                                      fg_color="#1A1A1A", hover_color="#333333", border_width=1, border_color="#3A3A3A", text_color="#A0A0A0",
                                      command=self.toggle_language, corner_radius=8)
        self.btn_lang.place(x=25, y=10)
        
        # Painel central movido ligeiramente para baixo (pady top = 45) para n colidir com a flag
        self.main_frame = ctk.CTkFrame(self, fg_color="#1E1E1E", corner_radius=16, border_width=1, border_color="#2A2A2A")
        self.main_frame.pack(fill="both", expand=True, padx=25, pady=(45, 25))
        
        # Cabecalhos
        self.header = ctk.CTkLabel(self.main_frame, text="", font=TITLE_FONT, text_color="#FFFFFF")
        self.header.pack(pady=(30, 2))
        self.subtitle = ctk.CTkLabel(self.main_frame, text="", font=SUB_FONT, text_color="#888888")
        self.subtitle.pack(pady=(0, 25))
        
        # Parse JSON
        self.data = load_or_create_settings()
        env_data = self.data.get("env", {})
            
        current_model = env_data.get("OPENAI_MODEL", "")
        current_key = env_data.get("OPENAI_API_KEY", "")
        
        self.inputs_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.inputs_frame.pack(fill="x", padx=40)
        
        # --- NOME DO MODELO ---
        self.lbl_model = ctk.CTkLabel(self.inputs_frame, text="", font=LABEL_FONT, text_color="#888888")
        self.lbl_model.pack(anchor="w", pady=(0, 4))
        
        self.model_container = ctk.CTkFrame(self.inputs_frame, fg_color="transparent")
        self.model_container.pack(fill="x", pady=(0, 15))
        
        self.entry_model = ctk.CTkEntry(self.model_container, height=42, font=MAIN_FONT, fg_color="#2D2D2D", border_color="#3A3A3A", corner_radius=8, text_color="#FFFFFF")
        self.entry_model.pack(side="left", fill="x", expand=True, padx=(0, 8))
        self.entry_model.insert(0, current_model)
        
        self.btn_paste_model = ctk.CTkButton(self.model_container, text="📋", font=ICON_FONT, width=42, height=42,
                                             fg_color="#333333", hover_color="#555555", corner_radius=8,
                                             command=lambda: self.paste_to_entry(self.entry_model))
        self.btn_paste_model.pack(side="left", padx=(0, 8))
        
        self.btn_models = ctk.CTkButton(self.model_container, text="", font=("Inter", 12, "bold"), height=42, width=105,
                                        fg_color="#4F46E5", hover_color="#4338CA", corner_radius=8, text_color="#FFFFFF",
                                        command=self.open_models_url)
        self.btn_models.pack(side="left")

        # --- CHAVE DE API ---
        self.lbl_key = ctk.CTkLabel(self.inputs_frame, text="", font=LABEL_FONT, text_color="#888888")
        self.lbl_key.pack(anchor="w", pady=(0, 4))
        
        self.key_container = ctk.CTkFrame(self.inputs_frame, fg_color="transparent")
        self.key_container.pack(fill="x", pady=(0, 8))
        
        self.entry_key = ctk.CTkEntry(self.key_container, height=42, show="●", font=MAIN_FONT, fg_color="#2D2D2D", border_color="#3A3A3A", corner_radius=8, text_color="#FFFFFF")
        self.entry_key.pack(side="left", fill="x", expand=True, padx=(0, 8))
        self.entry_key.insert(0, current_key)
        
        self.btn_paste_key = ctk.CTkButton(self.key_container, text="📋", font=ICON_FONT, width=42, height=42,
                                            fg_color="#333333", hover_color="#555555", corner_radius=8,
                                            command=lambda: self.paste_to_entry(self.entry_key))
        self.btn_paste_key.pack(side="left", padx=(0, 8))
        
        self.btn_keys = ctk.CTkButton(self.key_container, text="", font=("Inter", 12, "bold"), height=42, width=125,
                                      fg_color="#4F46E5", hover_color="#4338CA", corner_radius=8, text_color="#FFFFFF",
                                      command=self.open_keys_url)
        self.btn_keys.pack(side="left")
        
        self.check_var = ctk.StringVar(value="off")
        self.checkbox = ctk.CTkCheckBox(self.inputs_frame, text="", font=("Inter", 12, "bold"), text_color="#BBBBBB",
                                        command=self.toggle_show, variable=self.check_var, onvalue="on", offvalue="off",
                                        checkbox_width=20, checkbox_height=20, border_color="#555555", hover_color="#777777", fg_color="#FFFFFF", checkmark_color="#000000", corner_radius=6)
        self.checkbox.pack(anchor="w", pady=(0, 20))
        
        # --- AÇÕES ---
        self.actions_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.actions_frame.pack(fill="x", padx=40, pady=(5, 0))
        
        self.btn_save = ctk.CTkButton(self.actions_frame, text="", command=self.save_data, 
                                      font=("Inter", 14, "bold"), height=46, fg_color="#FFFFFF", text_color="#000000", hover_color="#E0E0E0", corner_radius=8)
        self.btn_save.pack(fill="x", pady=(0, 10))
        
        self.status = ctk.CTkLabel(self.main_frame, text="", font=("Inter", 13, "bold"))
        self.status.pack(pady=(15, 0))

        # Inicia pintando todos os Labels na lingua nativa escolhida
        self.refresh_language()

    def refresh_language(self):
        t = self.i18n[self.current_lang]
        self.title(t["window"])
        self.header.configure(text=t["header"])
        self.subtitle.configure(text=t["subtitle"])
        self.lbl_model.configure(text=t["model_lbl"])
        self.lbl_key.configure(text=t["key_lbl"])
        self.btn_models.configure(text=t["btn_free"])
        self.btn_keys.configure(text=t["btn_gen"])
        self.checkbox.configure(text=t["check_vis"])
        self.btn_save.configure(text=t["btn_save"])
        self.btn_lang.configure(text=t["lang_btn"])
        self.status.configure(text="")

    def toggle_language(self):
        self.current_lang = "en" if self.current_lang == "pt" else "pt"
        self.refresh_language()

    def paste_to_entry(self, target_entry):
        try:
            content = self.clipboard_get()
            target_entry.delete(0, "end")
            target_entry.insert(0, content.strip())
        except Exception:
            pass

    def open_models_url(self):
        webbrowser.open("https://openrouter.ai/models?q=free")

    def open_keys_url(self):
        webbrowser.open("https://openrouter.ai/workspaces/default/keys")

    def toggle_show(self):
        if self.check_var.get() == "on":
            self.entry_key.configure(show="")
        else:
            self.entry_key.configure(show="●")

    def save_data(self):
        if self.data is None:
            self.data = {}
        if "env" not in self.data:
            self.data["env"] = {}
            
        self.data["env"]["OPENAI_MODEL"] = self.entry_model.get().strip()
        self.data["env"]["OPENAI_API_KEY"] = self.entry_key.get().strip()
        save_settings(self.data)
        
        t = self.i18n[self.current_lang]
        self.status.configure(text=t["msg_save"], text_color="#10B981")
        self.after(3000, lambda: self.status.configure(text=""))

if __name__ == "__main__":
    app = App()
    app.mainloop()
