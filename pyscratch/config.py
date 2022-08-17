import os.path
import json
import zipfile

class Config:
    IMAGES: dict[str, str]
    
    @classmethod
    def load_images(cls, data):
        for img in data["images"]:
            cls.IMAGES[img["name"]] = img["file"]
    
    @classmethod
    def parse_project_file(cls, file_path: str):
        if os.path.splitext(file_path)[1] != ".pysc" or not os.path.isfile(file_path) or not zipfile.is_zipfile(file_path):
            return

        with zipfile.ZipFile(file_path, "r") as project:
            project_name = project.namelist()[0].split("/")[0]
            with project.open(f"{project_name}/project.json") as project_info:
                data = json.load(project_info)
                
 

if __name__ == "__main__":
    Config.parse_project_file("C:\\Users\\sebi_\\Desktop\\python\\pyscratch\\TestProject.pysc")