
from pydantic import BaseModel, Field
class IngredienteSchema(BaseModel):
    nome: str

class ReceitaQuery(BaseModel):
    nome: str
    ingredientes: list[IngredienteSchema]
    descricao: str
    like: bool
    imagemBase64: str

class ReceitaId(BaseModel):
    id: int = Field(..., description='receita id')