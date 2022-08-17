class Config:
    IMAGES: dict[str, str]
    
    @classmethod
    def load_images(cls, data):
        for img in data["images"]:
            cls.IMAGES[img["name"]] = img["file"]
    