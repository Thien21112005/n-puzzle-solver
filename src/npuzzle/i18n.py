"""Interface text and number formats in every supported language."""

DEFAULT_LANGUAGE = "vi"

LANGUAGE_NAMES = {"vi": "Tiếng Việt", "en": "English"}

_SEPARATORS = {"vi": (".", ","), "en": (",", ".")}

STRINGS = {
    "vi": {
        "title": "N-Puzzle",
        "title_won": "N-Puzzle - Bạn đã thắng!",
        "comparison": "So sánh thuật toán",
        "col_algorithm": "Thuật toán",
        "col_nodes": "Node",
        "col_steps": "Bước",
        "col_time": "Thời gian",
        "col_memory": "Bộ nhớ (ước tính)",
        "table_note": "Kết quả trên bàn vừa giải. Số màu xanh là tốt nhất.",
        "table_empty": "Chọn một thuật toán rồi bấm Giải để ghi kết quả.",
        "solve_with": "Giải bằng {algorithm}",
        "cancel": "Hủy",
        "skip": "Tua hết",
        "shuffle": "Xáo bàn",
        "reset": "Đặt lại",
        "moves": "Số bước",
        "hint": "Dùng phím mũi tên hoặc bấm vào ô cạnh chỗ trống để chơi.",
        "searching": "Đang tìm lời giải bằng {algorithm}...",
        "playing": "Đang giải bằng {algorithm}: còn {count} bước",
        "no_solution": "{algorithm} không tìm thấy lời giải.",
        "won": "Bạn đã thắng sau {count} bước!",
        "solved": "{algorithm} đã giải xong sau {count} bước.",
        "picture_on": "Đang chơi với ảnh",
        "picture_off": "Đang chơi với số",
        "picture_hint": "Ghép bằng ảnh của bạn.",
        "reference": "Hình hoàn chỉnh",
        "choose_image": "Chọn ảnh",
        "change_image": "Đổi ảnh",
        "remove_image": "Bỏ ảnh",
        "language": "Ngôn ngữ",
        "dialog_title": "Chọn hình ảnh",
        "dialog_filter": "Tệp hình ảnh",
        "image_error": "Không mở được ảnh này. Hãy chọn tệp JPG, PNG hoặc BMP khác.",
    },
    "en": {
        "title": "N-Puzzle",
        "title_won": "N-Puzzle - You won!",
        "comparison": "Algorithm comparison",
        "col_algorithm": "Algorithm",
        "col_nodes": "Nodes",
        "col_steps": "Moves",
        "col_time": "Time",
        "col_memory": "Memory (estimate)",
        "table_note": "Results for the board last solved. Green marks the best.",
        "table_empty": "Pick an algorithm, then press Solve to record a result.",
        "solve_with": "Solve with {algorithm}",
        "cancel": "Cancel",
        "skip": "Skip",
        "shuffle": "Shuffle",
        "reset": "Reset",
        "moves": "Moves",
        "hint": "Use the arrow keys or click a tile next to the gap to play.",
        "searching": "Searching with {algorithm}...",
        "playing": "Solving with {algorithm}: {count} moves left",
        "no_solution": "{algorithm} found no solution.",
        "won": "You won in {count} moves!",
        "solved": "{algorithm} finished in {count} moves.",
        "picture_on": "Playing with a picture",
        "picture_off": "Playing with numbers",
        "picture_hint": "Or use your own picture.",
        "reference": "Finished picture",
        "choose_image": "Picture",
        "change_image": "Change",
        "remove_image": "Remove",
        "language": "Language",
        "dialog_title": "Choose a picture",
        "dialog_filter": "Image files",
        "image_error": "This picture could not be opened. Choose a JPG, PNG or BMP file.",
    },
}


class Translator:
    def __init__(self, language: str = DEFAULT_LANGUAGE):
        self.language = language if language in STRINGS else DEFAULT_LANGUAGE

    def __call__(self, key: str, **values) -> str:
        return STRINGS[self.language][key].format(**values)


def format_count(value: int, language: str) -> str:
    return f"{value:,}".replace(",", _SEPARATORS[language][0])


def _decimal(value: float, digits: int, language: str) -> str:
    return f"{value:.{digits}f}".replace(".", _SEPARATORS[language][1])


def format_seconds(seconds: float, language: str) -> str:
    if seconds < 1:
        milliseconds = seconds * 1000
        return f"{_decimal(milliseconds, 1 if milliseconds < 10 else 0, language)} ms"
    return f"{_decimal(seconds, 2, language)} s"


def format_bytes(value: int, language: str) -> str:
    """Format an estimate, which the approximate sign makes explicit."""
    if value < 1024 * 1024:
        return f"≈ {_decimal(value / 1024, 0, language)} KB"
    return f"≈ {_decimal(value / (1024 * 1024), 1, language)} MB"
