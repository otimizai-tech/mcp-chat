from mcp.server.fastmcp import FastMCP
import asyncio
from gitingest import ingest_async
from typing import Optional, List, Union, Dict, Any, Tuple

mcp = FastMCP("teste")

@mcp.tool()
def add(a: int, b: int) -> int:
    """Soma dois números"""
    return a + b

@mcp.tool()
def to_uppercase(text: str) -> str:
    """Converte texto para maiúsculas"""
    return text.upper()

@mcp.tool()
def company_name() -> str:
    """Retorna o nome da empresa quando solicitado"""
    return "Otimizai"

@mcp.tool()
async def ingest_repository(
    url: str, 
    include_patterns: Optional[Union[str, List[str]]] = None,
    exclude_patterns: Optional[Union[str, List[str]]] = None,
    branch: Optional[str] = None
) -> Dict[str, Any]:
    """
    Ingere um repositório Git e retorna seu conteúdo, filtrando apenas arquivos Markdown (.md).
    
    Args:
        url: URL do repositório Git
        include_patterns: Padrões adicionais de arquivos a incluir (além de .md)
        exclude_patterns: Padrões de arquivos a excluir
        branch: Nome da branch (opcional)
        
    Returns:
        Dicionário contendo summary, tree e content do repositório com apenas documentação markdown
    """
    # Sempre incluir arquivos .md
    md_pattern = "*.md"
    
    # Processar include_patterns para garantir que .md esteja sempre incluído
    if include_patterns is None:
        # Se não houver padrões, usar apenas .md
        include_patterns_set = {md_pattern}
    elif isinstance(include_patterns, str):
        # Se for uma string, converter para set e adicionar .md
        include_patterns_set = {include_patterns, md_pattern}
    else:
        # Se for uma lista, converter para set e adicionar .md
        include_patterns_set = set(include_patterns)
        include_patterns_set.add(md_pattern)
    
    exclude_patterns_set = set(exclude_patterns) if isinstance(exclude_patterns, list) else exclude_patterns
    
    # Processar URLs do GitHub com formato /tree/branch/path
    # Exemplo: https://github.com/otimizai-tech/mcp-chat/tree/main/backend
    import re
    
    # Verificar se é uma URL do GitHub com formato /tree/
    github_tree_pattern = r'https://github\.com/([^/]+)/([^/]+)/tree/([^/]+)(/.*)?'
    match = re.match(github_tree_pattern, url)
    
    if match:
        # Extrair informações da URL
        user, repo, branch_name, subpath = match.groups()
        
        # Reconstruir a URL base do repositório
        base_url = f"https://github.com/{user}/{repo}"
        
        # Usar o branch da URL se não foi especificado explicitamente
        if branch is None:
            branch = branch_name
        
        # Se houver um subpath, adicionar ao include_patterns para filtrar apenas esse diretório
        if subpath and subpath != '/':
            # Remover a barra inicial e adicionar /**
            dir_pattern = subpath.lstrip('/') + '/**'
            
            # Adicionar o padrão de diretório ao conjunto de include_patterns
            include_patterns_set.add(dir_pattern)
        
        # Usar a URL base para a ingestão
        url = base_url
    
    summary, tree, content = await ingest_async(
        url,
        include_patterns=include_patterns_set,
        exclude_patterns=exclude_patterns_set,
        branch=branch
    )
    
    return {
        "summary": summary,
        "tree": tree,
        "content": content,
    }

if __name__ == "__main__":
    asyncio.run(mcp.run(transport="sse"))