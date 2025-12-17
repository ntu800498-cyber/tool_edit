
import whisper
from deep_translator import GoogleTranslator
import os

class OfflineVideoTranslator:
    def __init__(self, model_size="base"):
        # model_size có các mức: tiny, base, small, medium, large
        # 'base' phù hợp cho máy tính cấu hình trung bình
        print("Đang tải mô hình AI (lần đầu sẽ hơi lâu)...")
        self.model = whisper.load_model(model_size)

    def translate(self, video_path):
        print(f"--- Đang xử lý: {os.path.basename(video_path)} ---")
        
        # 1. Nhận diện giọng nói và lấy mốc thời gian (Speech-to-Text)
        # task="transcribe" để lấy ngôn ngữ gốc, hoặc task="translate" để ra tiếng Anh luôn
        result = self.model.transcribe(video_path)
        
        segments = result['segments']
        translated_segments = []
        
        translator = GoogleTranslator(source='auto', target='vi')

        print("Đang dịch thuật nội dung...")
        for seg in segments:
            start = seg['start']
            end = seg['end']
            text = seg['text']
            
            # 2. Dịch từng đoạn sang tiếng Việt
            translated_text = translator.translate(text)
            
            # Lưu kết quả kèm mốc thời gian
            line = f"[{self.format_time(start)} --> {self.format_time(end)}]: {translated_text}"
            translated_segments.append(line)
            print(line)

        return translated_segments

    def format_time(self, seconds):
        """Định dạng giây thành hh:mm:ss"""
        td = str(round(seconds, 2)).replace('.', ',')
        return td

# --- Chạy thử nghiệm ---
if __name__ == "__main__":
    # Thay 'video.mp4' bằng đường dẫn file của bạn
    engine = OfflineVideoTranslator(model_size="base")
    results = engine.translate("video_test.mp4")
    
    with open("sub_viet.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(results))
    print("\nĐã lưu bản dịch vào file sub_viet.txt")