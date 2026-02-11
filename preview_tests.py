from src.sm_blueprint_lib import preview, load_blueprint

bp = load_blueprint("sm lib output")
print(f"size: {len(list(bp.all_parts()))}")
preview(bp)
