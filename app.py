
from flask_openapi3 import Info, Tag
from flask_openapi3 import OpenAPI
from receita import Receita, db
from schemas import ReceitaId, ReceitaQuery
from flask_cors import CORS

info = Info(title="Receita API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"
db.init_app(app)

with app.app_context():
    db.create_all()

receita_tag = Tag(name="Receita", description="Uma receita")

@app.get("/receita/listar", summary="listar receitas", tags=[receita_tag])
def receita_listar_todas():
    """
    Consultar todas as receitas
    """
    try:
        receitas = db.session.query(Receita).all()
        data = [{
                'id': i.id,
                'nome': i.nome,
                'descricao': i.descricao,
                'ingredientes': i.ingredientes['data'],
                'imagemBase64': i.imagemBase64,
                'like': i.like
                 } for i in receitas]

        return  {"code": 200, "message": "ok", "data": data}
    
    except Exception as e:
        print(e)
        error_msg = "Não foi possível listar as receitas"
        return {"mesage": error_msg}, 400


@app.get("/receita/consulta/<int:id>", summary="consultar receita pelo id", tags=[receita_tag])
def receita_consultar_id(path: ReceitaId):
    """
    Consultar receita pelo id
    """
    try:
        receita = db.session.query(Receita).filter(Receita.id == path.id).first()
        if receita:
            data = {
                    'id': receita.id,
                    'nome': receita.nome,
                    'descricao': receita.descricao,
                    'ingredientes': receita.ingredientes['data'],
                    'imagemBase64': receita.imagemBase64,
                    'like': receita.like
                    }
            return {"code": 200, "message": "ok", "data" : data}
        else:
            return {"code": 200, "message": "Não existe receita com o id informado"}
    
    except Exception as e:
        print(e)
        error_msg = "Não foi possível encontrar a receita"
        return {"mesage": error_msg}, 400


@app.post("/receita/cadastrar", summary="cadastrar nova receita", tags=[receita_tag])
def receita_cadastrar(body: ReceitaQuery):
    """
    Cadastrar nova receita
    """
    nova_receia = Receita(
        nome=body.nome, 
        ingredientes={"data": [{"nome": i.nome} for i in body.ingredientes]}, 
        descricao=body.descricao,
        imagemBase64=body.imagemBase64,
        like=body.like)
    try:
        db.session.add(nova_receia)
        db.session.commit()
        return {"code": 0, "message": "ok"}
    
    except Exception as e:
        print(e)
        error_msg = "Não foi possível salvar uma nova receita :/"
        return {"mesage": error_msg}, 400


@app.put("/receita/editar/<int:id>", summary="editar receita", tags=[receita_tag])
def receita_editar(path: ReceitaId, body: ReceitaQuery):
    """
    Editar uma receita
    """
    try:
        receita = db.session.query(Receita).filter(Receita.id == path.id).first()
        if receita:
            receita.nome = body.nome
            receita.ingredientes ={"data": [{"nome": i.nome} for i in body.ingredientes]}
            receita.descricao = body.descricao
            receita.imagemBase64 = body.imagemBase64
            receita.like = body.like
            db.session.commit()

            return {"code": 200, "message": "Receita alterada com sucesso"}
        else:
            return {"code": 200, "message": "Não existe receita com o id informado."}
        
    except Exception as e:
        print(e)
        error_msg = "Não foi possível alterar a receita"
        return {"mesage": error_msg}, 400

@app.get("/receita/excluir/<int:id>", summary="excluir receita", tags=[receita_tag])
def receita_excluir(path: ReceitaId):
    """
    Excluir uma receita
    """
    try:
        count = db.session.query(Receita).filter(Receita.id == path.id).delete()
        db.session.commit()
        if count:
            return {"code": 200, "message": "Receita excluída com sucesso"}
        else:
            return {"code": 200, "message": "Não existe receita com o id informado."}
        
    except Exception as e:
        print(e)
        error_msg = "Não foi possível excluir a receita"
        return {"mesage": error_msg}, 400


@app.get("/receita/like/<int:id>", summary="like/unlike receita", tags=[receita_tag])
def receita_like(path: ReceitaId):
    """
    Gostar/Retirar gostar de uma receita
    """
    try:
        receita = db.session.query(Receita).filter(Receita.id == path.id).first()
        if receita:
            receita.like = not receita.like
            db.session.commit()

            return {"code": 200, "message": "Like/unlike com sucesso"}
        else:
            return {"code": 200, "message": "Não existe receita com o id informado."}
        
    except Exception as e:
        print(e)
        error_msg = "Não foi possível dar like/unlike na receita"
        return {"mesage": error_msg}, 400


if __name__ == "__main__":
    app.run(debug=True)

