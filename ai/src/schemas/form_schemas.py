from pydantic import BaseModel, Field
from typing import Optional, List


class PatientInfos(BaseModel):
    name: Optional[str] = Field(None, description="Name of the patient")
    surname: Optional[str] = Field(None, description="Surname of the patient")
    age: Optional[int] = Field(None, description="Age of the patient")
    id: Optional[str] = Field(None, description="TC identity number of the patient")


class FormUstBatinBT(BaseModel):
    """Şablon: Üst Batın BT (Upper abdomen CT)

    Bu model, LLM'den yapılacak çıkarım için beklenen alanları tanımlar. `findings` alanı
    raporda yer alması istenen detaylı bulguları içermelidir (örnek metin proje sahibinin
    gönderdiği sabit şablon olabilir veya LLM tarafından doldurulabilir)."""

    patient_informations: PatientInfos = Field(..., description="Informations of the relevant patient")
    examination: str = Field("Üst Batın BT", description="The examination type / modality")
    findings: str = Field(description="Detailed findings text that will be inserted into the report.")
    result: str = Field(description="The final conclusion or summary for the report.")
    dr_note: Optional[str] = Field(None, description="Additional doctor's notes, if any.")


class PatientTextChunk(BaseModel):
    patient_name: str = Field(description="The full name or a clear identifier of the detected patient (e.g., 'Ahmet Yılmaz').")
    related_text: str = Field(description="The combined text of all sentences from the entire transcript that relate only to this patient.")


class TranscriptAnalysis(BaseModel):
    patient_chunks: List[PatientTextChunk]