"""Pure strict response parser. No recovery or synthetic measured output."""
IDS='0123456789ABCDEFGHIJ'
def parse_native(raw,truncated=False):
    lines=[line.strip() for line in raw.splitlines() if line.strip()]
    reasons=[]
    if truncated:reasons.append('truncated')
    if len(lines)!=10:reasons.append('wrong_count')
    if any(line not in IDS or len(line)!=1 for line in lines):reasons.append('invalid_format_or_id')
    duplicate=len(lines)!=len(set(lines))
    if duplicate:reasons.append('duplicate')
    return {'valid':not reasons,'selected_ids':lines if not reasons else [],'parsed_lines':lines,'reasons':reasons,'duplicate':duplicate}
