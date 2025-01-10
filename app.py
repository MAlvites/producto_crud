from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List, Optional
import json
import os

## Base de datos
DATABASE_FILE = "productos.json"

class Producto(BaseModel):
    id: int
    nombre: str
    categoría: str
    precio: float
    stock: int

def load_productos():
    if not os.path.exists(DATABASE_FILE):
        return []
    with open(DATABASE_FILE, "r") as file:
        try:
            data = json.load(file)
            return [Producto(**item) for item in data]
        except json.JSONDecodeError:
            return []

def save_productos(productos: List[Producto]):
    with open(DATABASE_FILE, "w") as file:
        json.dump([producto.dict() for producto in productos], file)

def add_producto(producto: Producto):
    productos = load_productos()
    if any(p.nombre == producto.nombre for p in productos):
        raise HTTPException(status_code=400, detail="Ya existe un producto con ese nombre")
    if producto.precio <= 0:
        raise HTTPException(status_code=400, detail="El precio debe ser mayor que 0")
    if producto.stock < 0:
        raise HTTPException(status_code=400, detail="El stock no puede ser negativo")
    producto.id = len(productos) + 1
    productos.append(producto)
    save_productos(productos)

def update_producto(id: int, updated_producto: Producto):
    productos = load_productos()
    for index, producto in enumerate(productos):
        if producto.id == id:
            if any(p.nombre == producto.nombre for p in productos):
                raise HTTPException(status_code=400, detail="Ya existe un producto con ese nombre")
            if updated_producto.precio <= 0:
                raise HTTPException(status_code=400, detail="El precio debe ser mayor que 0")
            if updated_producto.stock < 0:
                raise HTTPException(status_code=400, detail="El stock no puede ser negativo")
            productos[index] = updated_producto
            save_productos(productos)
            return True
    return False

def delete_producto(id: int):
    productos = load_productos()
    productos = [producto for producto in productos if producto.id != id]
    save_productos(productos)
    return True

## Servidor Web
app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def productos(
    request: Request,
    min_price: Optional[str] = None,
    max_price: Optional[str] = None,
    categoria: Optional[str] = "",
    page: int = 1,
    size: int = 10
):
    productos = load_productos()

    # Reset filters if None, empty string or invalid values
    if min_price == "" or min_price is None:
        min_price = 0  # Default minimum price
    else:
        min_price = float(min_price)

    if max_price == "" or max_price is None:
        max_price = float('inf')  # Set max_price to infinity to remove the upper bound
    else:
        max_price = float(max_price)

    if not categoria:
        categoria = ""  # Default category (empty)

    # Filter by price
    productos = [p for p in productos if min_price <= p.precio <= max_price]

    # Filter by category
    if categoria:
        productos = [p for p in productos if categoria.lower() in p.categoría.lower()]

    # Pagination
    total_productos = len(productos)
    start = (page - 1) * size
    end = start + size
    productos_paginated = productos[start:end]
    total_pages = (total_productos // size) + (1 if total_productos % size > 0 else 0)

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "productos": productos_paginated,
            "page": page,
            "total_pages": total_pages,
            "min_price": min_price,
            "max_price": max_price,
            "categoria": categoria,
        }
    )

@app.get("/crear", response_class=HTMLResponse)
async def productos_crear(request: Request):
    return templates.TemplateResponse("modulos/productos/crear.html", context={"request": request})

@app.post("/crear/guardar")
async def productos_crear_guardar(
    request: Request,
    nombre: str = Form(...),
    categoría: str = Form(...),
    precio: float = Form(...),
    stock: int = Form(...),
):
    productos = load_productos()
    new_producto = Producto(id=len(productos) + 1, nombre=nombre, categoría=categoría, precio=precio, stock=stock)

    error_nombre = error_precio = error_stock = None
    if any(p.nombre == nombre for p in productos):
        error_nombre = "Ya existe un producto con ese nombre"
    if precio <= 0:
        error_precio = "El precio debe ser mayor que 0"
    if stock < 0:
        error_stock = "El stock no puede ser negativo"

    if error_nombre or error_precio or error_stock:
        return templates.TemplateResponse(
            "modulos/productos/crear.html",
            {
                "request": request,
                "error_nombre": error_nombre,
                "error_precio": error_precio,
                "error_stock": error_stock
            }
        )

    add_producto(new_producto)
    return RedirectResponse(url="/", status_code=303)

@app.get("/{id}/actualizar", response_class=HTMLResponse)
async def productos_actualizar(request: Request, id: int):
    productos = load_productos()
    producto = next((p for p in productos if p.id == id), None)
    if not producto:
        return RedirectResponse(url="/", status_code=303)
    return templates.TemplateResponse(
        name="modulos/productos/actualizar.html",
        context={"request": request, "producto": producto}
    )

@app.post("/{id}/actualizar/guardar")
async def productos_actualizar_guardar(
    request: Request,
    id: int,
    nombre: str = Form(...),
    categoría: str = Form(...),
    precio: float = Form(...),
    stock: int = Form(...),
):
    productos = load_productos()

    updated_producto = Producto(id=id, nombre=nombre, categoría=categoría, precio=precio, stock=stock)

    error_nombre = error_precio = error_stock = None
    if any(p.nombre == nombre for p in productos):
        error_nombre = "Ya existe un producto con ese nombre"
    if precio <= 0:
        error_precio = "El precio debe ser mayor que 0"
    if stock < 0:
        error_stock = "El stock no puede ser negativo"

    if error_precio or error_stock or error_nombre:
        return templates.TemplateResponse(
            "modulos/productos/actualizar.html",
            {
                "request": request,
                "producto": updated_producto,
                "error_nombre": error_nombre,
                "error_precio": error_precio,
                "error_stock": error_stock
            }
        )

    update_producto(id, updated_producto)
    return RedirectResponse(url="/", status_code=303)

@app.post("/{id}/eliminar")
async def productos_eliminar(id: int):
    if delete_producto(id):
        return RedirectResponse(url="/", status_code=303)
    return {"error": "Producto no encontrado"}
