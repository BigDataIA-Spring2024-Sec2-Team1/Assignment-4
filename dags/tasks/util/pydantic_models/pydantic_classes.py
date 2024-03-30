
from pathlib import Path
from pydantic import BaseModel, HttpUrl, ValidationError, constr, field_validator, FilePath

from typing import Optional

class URLClass(BaseModel):
    title: constr(min_length=1, max_length=200)
    topic: constr(min_length=1, max_length=200)
    published_year: int
    level: constr(pattern=r'^Level\s(I|II|III)$')
    introduction: Optional[str]
    learning_outcomes: Optional[str]
    summary: Optional[str]
    overview: Optional[str]
    link: HttpUrl

    @field_validator('published_year')
    @classmethod
    def validate_published_year(cls, value):
        if not (2018 <= value <= 2024):
            raise ValueError('Published year must be between 2018 and 2024')
        return value

    @field_validator('learning_outcomes')
    @classmethod
    def validate_learning_outcomes(cls, value):
        if len(value.split()) < 10:
            raise ValueError('Learning outcomes must be at least 10 words long')
        return value

    @field_validator('title')
    @classmethod
    def validate_title(cls, value):
        if not value.strip():
            raise ValueError('Title cannot be empty')
        return value

    @field_validator('topic')
    @classmethod
    def validate_topic(cls, value):
        if not value.strip():
            raise ValueError('Topic cannot be empty')
        return value

    @field_validator('level')
    @classmethod
    def validate_level(cls, value):
        if value not in ['Level I', 'Level II', 'Level III']:
            raise ValueError('Level must be one of: "Level I", "Level II", "Level III"')
        return value

    @field_validator('introduction')
    @classmethod
    def validate_introduction(cls, value):
        if value and len(value) < 50:
            raise ValueError('Introduction must be at least 50 characters long')
        return value

    @field_validator('summary')
    @classmethod
    def validate_summary(cls, value):
        if value and len(value.split()) < 10:
            raise ValueError('Summary must be at least 10 words long')
        return value

    @field_validator('overview')
    @classmethod
    def validate_overview(cls, value):
        if value and len(value.split()) < 10:
            raise ValueError('Overview must be at least 10 words long')
        return value

    @field_validator('link')
    @classmethod
    def validate_link(cls, value):
        if not str(value).startswith('https://www.cfainstitute.org'):
            raise ValueError('Link must start with "https://www.cfainstitute.org"')
        return value
    
    
class MetaDataPDFClass(BaseModel):
    text: constr(min_length=1)
    section_title: constr(min_length=1)
    file_path: Path
    # para:str
    # pages:str

    class Config:
        # To ignore extra fields in the CSV
        extra = 'ignore'
        
    @field_validator('text')
    @classmethod
    def validate_text(cls, value):
        if not value.strip():  # Check if text is not empty or whitespace
            raise ValueError('Text cannot be empty')
        return value

    @field_validator('section_title')
    @classmethod
    def validate_section_title(cls, value):
        if not value.strip():  # Check if section_title is not empty or whitespace
            raise ValueError('Section title cannot be empty')
        return value

    # @field_validator('file_path')
    # @classmethod
    # def validate_file_path(cls, value):
    #     if not value.exists():  # Check if file_path exists
    #         raise ValueError('File path does not exist')
    #     return value

class ContentPDFClass(BaseModel):
    file_name: constr(pattern=r'^[A-Za-z\s]+$')
    extracted_content:  str
