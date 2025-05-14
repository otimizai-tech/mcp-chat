from gitingest import ingest_async
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, List, Union

app = FastAPI()

class RepositoryRequest(BaseModel):
    url: str
    include_patterns: Optional[Union[str, List[str]]] = None  
    exclude_patterns: Optional[Union[str, List[str]]] = None
    branch: Optional[str] = None 
    
@app.get("/")
async def root():
    return {"message": "Gitingest server is running"}

@app.post("/ingest")
async def ingest_repository(repo: RepositoryRequest):
    # Sempre incluir arquivos .md
    md_pattern = "*.md"
    
    # Processar include_patterns para garantir que .md esteja sempre incluído
    if repo.include_patterns is None:
        # Se não houver padrões, usar apenas .md
        include_patterns = {md_pattern}
    elif isinstance(repo.include_patterns, str):
        # Se for uma string, converter para set e adicionar .md
        include_patterns = {repo.include_patterns, md_pattern}
    else:
        # Se for uma lista, converter para set e adicionar .md
        include_patterns = set(repo.include_patterns)
        include_patterns.add(md_pattern)
    
    exclude_patterns = set(repo.exclude_patterns) if isinstance(repo.exclude_patterns, list) else repo.exclude_patterns
    
    # Processar URLs do GitHub com formato /tree/branch/path
    # Exemplo: https://github.com/otimizai-tech/mcp-chat/tree/main/backend
    import re
    url = repo.url
    branch = repo.branch
    
    # Verificar se é uma URL do GitHub com formato /tree/
    github_tree_pattern = r'https://github\.com/([^/]+)/([^/]+)/tree/([^/]+)(/.*)?'
    match = re.match(github_tree_pattern, url)
    
    if match:
        # Extrair informações da URL
        user, repo_name, branch_name, subpath = match.groups()
        
        # Reconstruir a URL base do repositório
        base_url = f"https://github.com/{user}/{repo_name}"
        
        # Usar o branch da URL se não foi especificado explicitamente
        if branch is None:
            branch = branch_name
        
        # Se houver um subpath, adicionar ao include_patterns para filtrar apenas esse diretório
        if subpath and subpath != '/':
            # Remover a barra inicial e adicionar /**
            dir_pattern = subpath.lstrip('/') + '/**'
            
            # Adicionar o padrão de diretório ao conjunto de include_patterns
            include_patterns.add(dir_pattern)
        
        # Usar a URL base para a ingestão
        url = base_url
    
    summary, tree, content = await ingest_async(
        url,
        include_patterns=include_patterns,
        exclude_patterns=exclude_patterns,
        branch=branch
    )
    
    return {
        "summary": summary,
        "tree": tree,
        "content": content,
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)