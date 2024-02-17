import strawberry
import uvicorn

from contextlib import asynccontextmanager
from fastapi import FastAPI
from config import db
from app.Graphql.query import Query
from app.Graphql.mutation import Mutation

from strawberry.fastapi import GraphQLRouter

def init_app():
    apps = FastAPI(
        title="SkilledUp API",
        description="SkilledUp",
        version="0.1.0"
    )

    @apps.on_event("startup")
    async def startup():
        await db.create_all()

    @apps.on_event("shutdown")
    async def shutdown():
        await db.close()

    # add graphql router
    schema = strawberry.Schema(query=Query, mutation=Mutation)
    graphql_app = GraphQLRouter(schema=schema)
    apps.include_router(graphql_app, prefix="/graphql")

    return apps

app = init_app()

if __name__ == '__main__':
    uvicorn.run("main:app", host="localhost", port=8888, reload=True)