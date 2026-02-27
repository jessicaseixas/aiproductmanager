#!/usr/bin/env python3
"""
Script to update Jira tickets with content from TICKET.md files.
Converts markdown to Atlassian Document Format (ADF) and updates via REST API.
"""

import os
import re
import json
import base64
import urllib.request
import urllib.error
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

JIRA_BASE_URL = os.getenv('JIRA_BASE_URL')
JIRA_USER_EMAIL = os.getenv('JIRA_USER_EMAIL')
JIRA_API_TOKEN = os.getenv('JIRA_API_TOKEN')

# Feature folder to Jira key mapping (extracted from README.md files)
FEATURE_JIRA_MAP = {
    'auth-sign-in': 'SLA-526',
    'auth-sign-up': 'SLA-525',
    'auth-criar-organizacao': 'SLA-521',
    'auth-convidar-membros': 'SLA-522',
    'auth-gerenciar-usuarios': 'SLA-523',
    'auth-editar-organizacao': 'SLA-524',
    'auth-recuperacao-senha': 'SLA-527',
    'auth-editar-perfil': 'SLA-528',
    'auth-aceite-termos': 'SLA-556',
    'lead-aba-conversa': 'SLA-511',
    'lead-aba-detalhes': 'SLA-512',
    'lead-aba-anotacoes': 'SLA-513',
    'lead-aba-interesse': 'SLA-514',
    'whatsapp-embedded-signup': 'SLA-590',
    'whatsapp-profile-config': 'SLA-591',
    'assistant-config': 'SLA-592',
    'whatsapp-status': 'SLA-593',
    'integracao-portais-olx': 'SLA-418',
    'integracao-facebook-ads': 'SLA-419',
    'integracao-chaves-na-mao': 'SLA-455',
}


def markdown_to_adf(md_content: str) -> dict:
    """Convert markdown content to Atlassian Document Format (ADF)."""
    lines = md_content.split('\n')
    content = []
    i = 0

    while i < len(lines):
        line = lines[i]

        # Skip empty lines
        if not line.strip():
            i += 1
            continue

        # Horizontal rule
        if line.strip() == '---':
            content.append({"type": "rule"})
            i += 1
            continue

        # Code block
        if line.strip().startswith('```'):
            lang = line.strip()[3:] or None
            code_lines = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith('```'):
                code_lines.append(lines[i])
                i += 1
            i += 1  # Skip closing ```
            code_block = {"type": "codeBlock", "content": [{"type": "text", "text": '\n'.join(code_lines)}]}
            if lang:
                code_block["attrs"] = {"language": lang}
            content.append(code_block)
            continue

        # Blockquote
        if line.strip().startswith('>'):
            quote_lines = []
            while i < len(lines) and lines[i].strip().startswith('>'):
                quote_lines.append(lines[i].strip()[1:].strip())
                i += 1
            quote_text = ' '.join(quote_lines)
            content.append({
                "type": "blockquote",
                "content": [{"type": "paragraph", "content": parse_inline(quote_text)}]
            })
            continue

        # Headings
        heading_match = re.match(r'^(#{1,6})\s+(.+)$', line)
        if heading_match:
            level = len(heading_match.group(1))
            text = heading_match.group(2)
            content.append({
                "type": "heading",
                "attrs": {"level": level},
                "content": parse_inline(text)
            })
            i += 1
            continue

        # Bullet list
        if line.strip().startswith('* ') or line.strip().startswith('- '):
            list_items = []
            while i < len(lines) and (lines[i].strip().startswith('* ') or lines[i].strip().startswith('- ')):
                item_text = lines[i].strip()[2:]
                list_items.append({
                    "type": "listItem",
                    "content": [{"type": "paragraph", "content": parse_inline(item_text)}]
                })
                i += 1
            content.append({"type": "bulletList", "content": list_items})
            continue

        # Ordered list
        ordered_match = re.match(r'^\d+\.\s+(.+)$', line.strip())
        if ordered_match:
            list_items = []
            while i < len(lines) and re.match(r'^\d+\.\s+', lines[i].strip()):
                item_text = re.sub(r'^\d+\.\s+', '', lines[i].strip())
                list_items.append({
                    "type": "listItem",
                    "content": [{"type": "paragraph", "content": parse_inline(item_text)}]
                })
                i += 1
            content.append({"type": "orderedList", "content": list_items})
            continue

        # Table
        if '|' in line and i + 1 < len(lines) and '---' in lines[i + 1]:
            table_rows = []
            # Header row
            headers = [cell.strip() for cell in line.split('|')[1:-1]]
            header_cells = []
            for h in headers:
                header_cells.append({
                    "type": "tableHeader",
                    "attrs": {},
                    "content": [{"type": "paragraph", "content": parse_inline(h)}]
                })
            table_rows.append({"type": "tableRow", "content": header_cells})
            i += 2  # Skip header and separator

            # Data rows
            while i < len(lines) and '|' in lines[i]:
                cells = [cell.strip() for cell in lines[i].split('|')[1:-1]]
                row_cells = []
                for cell in cells:
                    row_cells.append({
                        "type": "tableCell",
                        "attrs": {},
                        "content": [{"type": "paragraph", "content": parse_inline(cell)}]
                    })
                table_rows.append({"type": "tableRow", "content": row_cells})
                i += 1

            content.append({
                "type": "table",
                "attrs": {"isNumberColumnEnabled": False, "layout": "default"},
                "content": table_rows
            })
            continue

        # Regular paragraph
        content.append({
            "type": "paragraph",
            "content": parse_inline(line)
        })
        i += 1

    return {"version": 1, "type": "doc", "content": content}


def parse_inline(text: str) -> list:
    """Parse inline markdown formatting (bold, italic, code, links)."""
    if not text:
        return [{"type": "text", "text": ""}]

    result = []
    remaining = text

    while remaining:
        # Bold **text**
        bold_match = re.match(r'^(.*?)\*\*(.+?)\*\*(.*)$', remaining)
        if bold_match:
            if bold_match.group(1):
                result.extend(parse_inline(bold_match.group(1)))
            result.append({"type": "text", "text": bold_match.group(2), "marks": [{"type": "strong"}]})
            remaining = bold_match.group(3)
            continue

        # Inline code `code`
        code_match = re.match(r'^(.*?)`(.+?)`(.*)$', remaining)
        if code_match:
            if code_match.group(1):
                result.extend(parse_inline(code_match.group(1)))
            result.append({"type": "text", "text": code_match.group(2), "marks": [{"type": "code"}]})
            remaining = code_match.group(3)
            continue

        # Link [text](url)
        link_match = re.match(r'^(.*?)\[(.+?)\]\((.+?)\)(.*)$', remaining)
        if link_match:
            if link_match.group(1):
                result.extend(parse_inline(link_match.group(1)))
            result.append({
                "type": "text",
                "text": link_match.group(2),
                "marks": [{"type": "link", "attrs": {"href": link_match.group(3)}}]
            })
            remaining = link_match.group(4)
            continue

        # Plain text
        result.append({"type": "text", "text": remaining})
        break

    return result if result else [{"type": "text", "text": ""}]


def update_jira_issue(key: str, adf_content: dict) -> bool:
    """Update Jira issue description via REST API using curl."""
    import subprocess
    import tempfile

    url = f"{JIRA_BASE_URL}/rest/api/3/issue/{key}"

    # Prepare authentication
    auth_string = f"{JIRA_USER_EMAIL}:{JIRA_API_TOKEN}"
    auth_bytes = base64.b64encode(auth_string.encode('utf-8')).decode('utf-8')

    # Prepare data
    data = json.dumps({"fields": {"description": adf_content}})

    # Write to temp file to avoid shell escaping issues
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        f.write(data)
        temp_file = f.name

    try:
        result = subprocess.run([
            'curl', '-s', '-w', '%{http_code}', '-X', 'PUT',
            '-H', f'Authorization: Basic {auth_bytes}',
            '-H', 'Content-Type: application/json',
            '-d', f'@{temp_file}',
            url
        ], capture_output=True, text=True)

        os.unlink(temp_file)

        # curl writes status code at the end
        status_code = result.stdout[-3:] if len(result.stdout) >= 3 else '0'
        return status_code == '204'
    except Exception as e:
        print(f"  Error updating {key}: {str(e)}")
        if os.path.exists(temp_file):
            os.unlink(temp_file)
        return False


def add_comment(key: str, message: str) -> bool:
    """Add a comment to a Jira issue using curl."""
    import subprocess
    import tempfile

    url = f"{JIRA_BASE_URL}/rest/api/3/issue/{key}/comment"

    auth_string = f"{JIRA_USER_EMAIL}:{JIRA_API_TOKEN}"
    auth_bytes = base64.b64encode(auth_string.encode('utf-8')).decode('utf-8')

    comment_body = {
        "body": {
            "version": 1,
            "type": "doc",
            "content": [{
                "type": "paragraph",
                "content": [{"type": "text", "text": message}]
            }]
        }
    }

    data = json.dumps(comment_body)

    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        f.write(data)
        temp_file = f.name

    try:
        result = subprocess.run([
            'curl', '-s', '-w', '%{http_code}', '-X', 'POST',
            '-H', f'Authorization: Basic {auth_bytes}',
            '-H', 'Content-Type: application/json',
            '-d', f'@{temp_file}',
            url
        ], capture_output=True, text=True)

        os.unlink(temp_file)

        status_code = result.stdout[-3:] if len(result.stdout) >= 3 else '0'
        return status_code == '201'
    except Exception as e:
        print(f"  Error adding comment to {key}: {str(e)}")
        if os.path.exists(temp_file):
            os.unlink(temp_file)
        return False


def main():
    """Main function to process all TICKET.md files and update Jira."""
    base_path = Path(__file__).parent.parent / 'context' / 'our-product' / 'features' / 'planned'

    print("Updating Jira tickets with bullet points (replacing checkboxes)...\n")

    success_count = 0
    error_count = 0

    for feature_name, jira_key in FEATURE_JIRA_MAP.items():
        ticket_path = base_path / feature_name / 'TICKET.md'

        if not ticket_path.exists():
            print(f"[SKIP] {jira_key} ({feature_name}): TICKET.md not found")
            continue

        print(f"[PROCESSING] {jira_key} ({feature_name})...")

        # Read markdown content
        with open(ticket_path, 'r', encoding='utf-8') as f:
            md_content = f.read()

        # Convert to ADF
        adf_content = markdown_to_adf(md_content)

        # Update Jira
        if update_jira_issue(jira_key, adf_content):
            # Add comment documenting the change
            add_comment(jira_key, "Atualizado via script: checkboxes substituídos por bullet points")
            print(f"  [OK] {jira_key} updated successfully")
            success_count += 1
        else:
            print(f"  [ERROR] Failed to update {jira_key}")
            error_count += 1

    print(f"\n{'='*50}")
    print(f"Summary: {success_count} updated, {error_count} errors")


if __name__ == '__main__':
    main()
