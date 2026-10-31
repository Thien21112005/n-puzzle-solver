"""Interface text in every supported language."""

DEFAULT_LANGUAGE = "vi"

LANGUAGE_NAMES = {"vi": "Tiếng Việt", "en": "English"}

STRINGS = {
    "vi": {
        "title": "Trò chơi 8 ô",
        "title_won": "Trò chơi 8 ô - Bạn đã thắng!",
        "shuffle": "Xáo bàn",
        "choose_image": "Chọn ảnh",
        "solve": "Giải",
        "cancel": "Hủy",
        "skip": "Tua hết",
        "moves": "Số bước: {count}",
        "searching": "Đang tìm lời giải bằng {algorithm}...",
        "playing": "Đang giải bằng {algorithm}: còn {count} bước",
        "no_solution": "{algorithm} không tìm thấy lời giải",
        "won": "Bạn đã thắng!",
        "reference": "Hình hoàn chỉnh",
        "dialog_title": "Chọn hình ảnh",
        "dialog_filter": "Tệp hình ảnh",
        "error_title": "Lỗi",
        "image_error": "Không thể tải hình ảnh. Vui lòng chọn tệp hợp lệ.",
    },
    "en": {
        "title": "8 Puzzle",
        "title_won": "8 Puzzle - You won!",
        "shuffle": "Shuffle",
        "choose_image": "Picture",
        "solve": "Solve",
        "cancel": "Cancel",
        "skip": "Skip",
        "moves": "Moves: {count}",
        "searching": "Searching with {algorithm}...",
        "playing": "Solving with {algorithm}: {count} moves left",
        "no_solution": "{algorithm} found no solution",
        "won": "You won!",
        "reference": "Finished picture",
        "dialog_title": "Choose a picture",
        "dialog_filter": "Image files",
        "error_title": "Error",
        "image_error": "This picture could not be loaded. Please choose a valid file.",
    },
}


class Translator:
    def __init__(self, language: str = DEFAULT_LANGUAGE):
        self.language = language if language in STRINGS else DEFAULT_LANGUAGE

    def __call__(self, key: str, **values) -> str:
        return STRINGS[self.language][key].format(**values)
