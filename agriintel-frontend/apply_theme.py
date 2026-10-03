import re
import glob

with open("src/index.css", "r", encoding="utf-8") as f:
    css = f.read()

# 1. Imports and root
css = re.sub(
    r"@import url\('.*?'\);\n\n:root \{.*?\n\}",
    """@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:wght@400;500;600;700;800&display=swap');

:root {
  --bg-dark: #F9F8F6;
  --bg-gradient: none;
  --surface: #FFFFFF;
  --surface-border: #E5E0D8;
  --surface-hover: rgba(11, 43, 38, 0.05);
  --primary: #0B2B26;
  --primary-hover: #164C43;
  --text-main: #0B2B26;
  --text-muted: #5C6F66;
  --error: #D94841;
  --shadow: 0 10px 25px -5px rgba(11, 43, 38, 0.05);
  
  font-family: 'Inter', system-ui, sans-serif;
  color: var(--text-main);
  background: var(--bg-dark);
  min-height: 100vh;
  margin: 0;
  display: flex;
  flex-direction: column;
  -webkit-font-smoothing: antialiased;
}

h1, h2, h3, .auth-title, .nav-brand {
  font-family: 'Playfair Display', serif;
}""",
    css,
    flags=re.DOTALL
)

# 2. Navbar
css = re.sub(
    r"\.navbar \{.*?\n\}",
    """.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 40px;
  background: rgba(249, 248, 246, 0.85);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid var(--surface-border);
  position: sticky;
  top: 0;
  z-index: 100;
}""",
    css,
    flags=re.DOTALL
)

# 3. Nav-brand
css = re.sub(
    r"\.nav-brand \{.*?\n\}",
    """.nav-brand {
  font-size: 1.75rem;
  font-weight: 700;
  color: var(--primary);
  text-decoration: none;
}""",
    css,
    flags=re.DOTALL
)

# 4. Auth-container
css = re.sub(
    r"\.auth-container \{.*?\n\}",
    """.auth-container {
  background: var(--surface);
  border: 1px solid var(--surface-border);
  border-radius: 12px;
  padding: 48px;
  width: 100%;
  max-width: 360px;
  box-shadow: var(--shadow);
  animation: floatUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}""",
    css,
    flags=re.DOTALL
)

# 5. Auth-title
css = re.sub(
    r"\.auth-title \{.*?\n\}",
    """.auth-title {
  font-size: 3rem;
  font-weight: 700;
  margin: 0 0 8px 0;
  color: var(--primary);
  font-family: 'Playfair Display', serif;
  letter-spacing: -0.02em;
}""",
    css,
    flags=re.DOTALL
)

# 6. Input field
css = re.sub(
    r"\.input-field \{.*?\n\}",
    """.input-field {
  background: #FFFFFF;
  border: 1px solid #D1D5DB;
  border-radius: 8px;
  padding: 14px 16px;
  color: var(--text-main);
  font-family: inherit;
  font-size: 1rem;
  transition: all 0.2s ease;
  outline: none;
  width: 100%;
  box-sizing: border-box;
}""",
    css,
    flags=re.DOTALL
)

css = re.sub(
    r"\.input-field:focus \{.*?\n\}",
    """.input-field:focus {
  border-color: var(--primary);
  background: #FFFFFF;
  box-shadow: 0 0 0 3px rgba(11, 43, 38, 0.1);
}""",
    css,
    flags=re.DOTALL
)

# 7. Market card
css = re.sub(
    r"\.market-card \{.*?\n\}",
    """.market-card {
  background: #FFFFFF;
  border: 1px solid var(--surface-border);
  border-radius: 12px;
  padding: 24px;
  transition: transform 0.2s, box-shadow 0.2s;
}""",
    css,
    flags=re.DOTALL
)

css = re.sub(
    r"\.market-card:hover \{.*?\n\}",
    """.market-card:hover {
  transform: translateY(-4px);
  background: #FFFFFF;
  box-shadow: var(--shadow);
  border-color: var(--primary);
}""",
    css,
    flags=re.DOTALL
)

css = re.sub(
    r"\.market-crop-name \{.*?\n\}",
    """.market-crop-name {
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 4px;
  color: var(--primary);
}""",
    css,
    flags=re.DOTALL
)

# 8. Score card
css = re.sub(
    r"\.score-card \{.*?\n\}",
    """.score-card {
  padding: 20px;
  border-radius: 12px;
  background: #FFFFFF;
  border: 1px solid var(--surface-border);
}""",
    css,
    flags=re.DOTALL
)

css = re.sub(
    r"\.score-card\.healthy \{.*?\n\}",
    """.score-card.healthy {
  background: rgba(16, 185, 129, 0.05);
  border-color: rgba(16, 185, 129, 0.2);
}""",
    css,
    flags=re.DOTALL
)

css = re.sub(
    r"\.score-card\.stressed \{.*?\n\}",
    """.score-card.stressed {
  background: rgba(217, 72, 65, 0.05);
  border-color: rgba(217, 72, 65, 0.2);
}""",
    css,
    flags=re.DOTALL
)

# 9. Assistant components
css = re.sub(
    r"\.assistant-container \{.*?\n\}",
    """.assistant-container {
  display: flex;
  flex-direction: column;
  height: calc(100vh - 120px);
  max-width: 900px;
  margin: 0 auto;
  background: var(--surface);
  border: 1px solid var(--surface-border);
  border-radius: 12px;
  overflow: hidden;
  box-shadow: var(--shadow);
}""",
    css,
    flags=re.DOTALL
)

css = re.sub(
    r"\.assistant-header \{.*?\n\}",
    """.assistant-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  background: var(--bg-dark);
  border-bottom: 1px solid var(--surface-border);
}""",
    css,
    flags=re.DOTALL
)

css = re.sub(
    r"\.chat-input-area \{.*?\n\}",
    """.chat-input-area {
  padding: 20px 24px;
  background: var(--bg-dark);
  border-top: 1px solid var(--surface-border);
  display: flex;
  gap: 12px;
  align-items: center;
}""",
    css,
    flags=re.DOTALL
)

css = re.sub(
    r"\.chat-input-area input \{.*?\n\}",
    """.chat-input-area input {
  flex: 1;
  background: var(--surface);
  border: 1px solid var(--surface-border);
  border-radius: 8px;
  padding: 14px 20px;
  color: var(--text-main);
  font-size: 1.05rem;
  font-family: inherit;
  outline: none;
  transition: all 0.3s;
}""",
    css,
    flags=re.DOTALL
)

css = re.sub(r"\.assistant-title-group h2 \{.*?\}", ".assistant-title-group h2 { margin: 0; font-size: 1.5rem; color: var(--primary); }", css, flags=re.DOTALL)
css = re.sub(r"\.chat-message\.user \{.*?\}", ".chat-message.user { align-self: flex-end; flex-direction: row; }", css, flags=re.DOTALL)
css = re.sub(r"\.chat-bubble\.user \{.*?\}", ".chat-bubble.user { background: var(--primary); color: white; border-bottom-right-radius: 4px; }", css, flags=re.DOTALL)
css = re.sub(r"\.chat-bubble\.bot \{.*?\}", ".chat-bubble.bot { background: #FFFFFF; border: 1px solid var(--surface-border); color: var(--text-main); border-bottom-left-radius: 4px; }", css, flags=re.DOTALL)

# 10. Farm Sidebar
css = re.sub(
    r"\.farm-sidebar \{.*?\n\}",
    """.farm-sidebar {
  width: 100%;
  max-width: 420px;
  background: var(--surface);
  border-right: 1px solid var(--surface-border);
  padding: 40px 32px;
  display: flex;
  flex-direction: column;
  overflow-y: auto;
  z-index: 10;
  box-shadow: var(--shadow);
}""",
    css,
    flags=re.DOTALL
)
css = re.sub(
    r"\.farm-title \{.*?\n\}",
    """.farm-title {
  font-size: 2rem;
  font-weight: 800;
  margin: 0;
  color: var(--primary);
  font-family: 'Playfair Display', serif;
}""",
    css,
    flags=re.DOTALL
)

with open("src/index.css", "w", encoding="utf-8") as f:
    f.write(css)

# Also fix JSX inline styles globally
jsx_files = glob.glob("src/**/*.jsx", recursive=True)
for file in jsx_files:
    with open(file, "r", encoding="utf-8") as f:
        content = f.read()
    
    content = content.replace("background: 'rgba(0,0,0,0.2)'", "background: 'var(--bg-dark)'")
    content = content.replace("background: 'rgba(0, 0, 0, 0.25)'", "background: 'var(--bg-dark)'")
    content = content.replace("background: 'rgba(255,255,255,0.05)'", "background: 'var(--bg-dark)'")
    content = content.replace("color: '#fff'", "color: 'var(--text-main)'")
    
    with open(file, "w", encoding="utf-8") as f:
        f.write(content)

print("Theme successfully migrated to Figma Design System!")
