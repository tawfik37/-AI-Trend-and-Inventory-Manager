"""
Utility to clean and format LLM output for better readability
"""
import re


def clean_llm_output(text):
    """
    Clean LLM output by removing Markdown formatting and improving readability.
    
    Args:
        text: Raw LLM output with Markdown formatting
        
    Returns:
        Cleaned, readable text
    """
    # Remove Markdown headers (### -> just the text)
    text = re.sub(r'^#{1,6}\s+', '', text, flags=re.MULTILINE)
    
    # Remove bold markers (**text** -> text)
    text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)
    
    # Remove italic markers (*text* -> text)
    text = re.sub(r'\*([^*]+)\*', r'\1', text)
    
    # Remove bullet point markers (keep indentation)
    text = re.sub(r'^\s*[\*\-]\s+', '  • ', text, flags=re.MULTILINE)
    
    # Clean up multiple blank lines
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    return text.strip()


def format_llm_output_for_terminal(text):
    """
    Format LLM output for terminal with clean sections and bullets.
    
    Args:
        text: Raw LLM output
        
    Returns:
        Formatted text for terminal display
    """
    lines = []
    
    for line in text.split('\n'):
        # Section headers (lines starting with numbers like "1. ", "2. ")
        if re.match(r'^\d+\.\s+[A-Z]', line):
            section_title = re.sub(r'^\d+\.\s+', '', line).strip()
            lines.append('')
            lines.append('─' * 70)
            lines.append(f'  {section_title}')
            lines.append('─' * 70)
        
        # Sub-headers (lines with *Title:*)
        elif line.strip().startswith('*') and line.strip().endswith('*') and ':' in line:
            sub_title = line.strip().strip('*').strip()
            lines.append('')
            lines.append(f'  ▸ {sub_title}')
        
        # Bullet points
        elif re.match(r'^\s*[\*\-]', line):
            bullet_text = re.sub(r'^\s*[\*\-]\s+', '', line)
            # Remove bold markers
            bullet_text = re.sub(r'\*\*([^*]+)\*\*', r'\1', bullet_text)
            bullet_text = re.sub(r'\*([^*]+)\*', r'\1', bullet_text)
            lines.append(f'    • {bullet_text}')
        
        # Regular text
        elif line.strip():
            # Remove any remaining markdown
            clean_line = re.sub(r'\*\*([^*]+)\*\*', r'\1', line)
            clean_line = re.sub(r'\*([^*]+)\*', r'\1', clean_line)
            lines.append(f'    {clean_line.strip()}')
        
        # Blank lines
        else:
            lines.append('')
    
    return '\n'.join(lines)


def format_llm_output_for_html(text):
    """
    Format LLM output for HTML display with proper tags.
    
    Args:
        text: Raw LLM output with Markdown
        
    Returns:
        HTML formatted text
    """
    html_lines = []
    in_list = False
    
    for line in text.split('\n'):
        line = line.strip()
        
        if not line:
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            html_lines.append('<br>')
            continue
        
        # Headers (### Title)
        if line.startswith('###'):
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            title = line.replace('###', '').strip()
            html_lines.append(f'<h3 style="color: #667eea; margin-top: 20px; margin-bottom: 10px;">{title}</h3>')
        
        # Numbered sections (1. TITLE)
        elif re.match(r'^\d+\.\s+[A-Z]', line):
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            title = re.sub(r'^\d+\.\s+', '', line)
            html_lines.append(f'<h3 style="color: #667eea; margin-top: 25px; margin-bottom: 15px;">{title}</h3>')
        
        # Bullet points
        elif line.startswith('*') or line.startswith('-'):
            if not in_list:
                html_lines.append('<ul style="margin-left: 20px; line-height: 1.8;">')
                in_list = True
            
            # Remove bullet marker and bold/italic
            bullet_text = re.sub(r'^[\*\-]\s+', '', line)
            bullet_text = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', bullet_text)
            bullet_text = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', bullet_text)
            
            html_lines.append(f'<li>{bullet_text}</li>')
        
        # Regular text
        else:
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            
            # Convert bold and italic
            formatted_line = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', line)
            formatted_line = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', formatted_line)
            
            html_lines.append(f'<p style="margin: 10px 0;">{formatted_line}</p>')
    
    if in_list:
        html_lines.append('</ul>')
    
    return '\n'.join(html_lines)


# Example usage
if __name__ == "__main__":
    sample_text = """
### 1. REORDER SUGGESTIONS

*   **Immediate Reorders:**
    *   **Climbing Shoes:** Stock (40) is below reorder point. *Reorder immediately.*
    *   **Golf Shoes:** Trigger reorder now.

### 2. WAREHOUSING STRATEGY

*   **Trending Items:**
    *   Move Loafers to Zone A for better access.
    """
    
    print("CLEANED OUTPUT:")
    print("=" * 70)
    print(clean_llm_output(sample_text))
    print("\n\nFORMATTED FOR TERMINAL:")
    print("=" * 70)
    print(format_llm_output_for_terminal(sample_text))