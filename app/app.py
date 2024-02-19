from fastapi import FastAPI
from contextlib import asynccontextmanager
import strawberry
from strawberry.fastapi import GraphQLRouter
from strawberry.schema.config import StrawberryConfig
from app.Graphql.query import Query
from app.Graphql.mutation import Mutation
from app.Core.config import settings
from app.Db.session import db

schema = strawberry.Schema(query=Query,mutation=Mutation,config=StrawberryConfig(auto_camel_case=True))

@asynccontextmanager
async def lifespan(application: FastAPI):
    await db.create_all()
    yield
    await db.close()

def create_app():
    
    app = FastAPI(
        title=settings.PROJECT_TITLE,
        description=settings.PROJECT_DESCRIPTION,
        version=settings.PROJECT_VERSION,
        lifespan=lifespan
    )
    graphql_app = GraphQLRouter(schema)
    app.include_router(graphql_app, prefix="/graphql")

    return app