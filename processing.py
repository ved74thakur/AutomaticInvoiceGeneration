import base64
from dotenv import load_dotenv
import sys
from openai import OpenAI
import os


class ImageProcessor:
    def __init__(self, image_path):
        self.image_path = image_path
        self.base64_image = self.encode_image()

    def encode_image(self):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode('utf-8')
        

class DataExtraction:
    def __init__(self, api_key):
        load_dotenv()
        self.client = OpenAI(api_key=api_key)

    def extract_data(self, base64_image):
      response = self.client.chat.completions.create(
            model = "gpt-4o",
            messages = [
                {
                    "role": "user",
                    "content": [
                        { "type": "text", 
                        "text": ("Extract only the following fields from the image: Date, Vehicle No, Container Nos, Swal No, From, and To."
                                "Please return only these values in a concise format") },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}",
                            },

                }
            ]
                }
            ],
        )
        
      return response.choices[0].message.content

class DataParser:
    @staticmethod
    def convert_data(text):
        lines = text.strip().splitlines()
        data = {}
        for line in lines:
            key, value = line.split(":", 1)
            data[key.strip()] = value.strip()

        final_data = {
            'DATE' : data.get('Date', ''),
            'VEHICLE NO' : data.get('Vehicle No', ''),
            'CONTAINER NO': data.get('Container Nos', ' '),
            'SIZE': data.get('Swal No', ''),
            'FROM': data.get('From', ''),
            'TO': data.get('To', '')
        }

        return final_data

class InvoiceProcessor:
    def __init__(self, image_path, api_key):
        self.image_processor = ImageProcessor(image_path)
        self.data_extractor = DataExtraction(api_key)

    def process_invoice(self):
        base64_image = self.image_processor.base64_image
        extracted_text = self.data_extractor.extract_data(base64_image)
        return DataParser.convert_data(extracted_text)
    
image_path = "InvoiceCopy.jpg"
api_key = os.getenv('OPEN_API_KEY')

invoice_processor = InvoiceProcessor(image_path, api_key)


if __name__ == "__main__":
    
    final_data = invoice_processor.process_invoice()
    
            
        