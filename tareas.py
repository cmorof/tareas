import argparse
import json
from pathlib import Path

from rich.console import Console
from rich.table import Table

ARCHIVO = Path.home() / ".tareas.json"
console = Console()


def cargar():
    if ARCHIVO.exists():
        return json.loads(ARCHIVO.read_text(encoding="utf-8"))
    return []


def guardar(tareas):
    ARCHIVO.write_text(
        json.dumps(tareas, indent=2, ensure_ascii=False), encoding="utf-8"
    )


def anadir(texto):
    tareas = cargar()
    tareas.append({"texto": texto, "hecha": False})
    guardar(tareas)
    console.print(f"[green]Añadida:[/green] {texto}")


def listar():
    tareas = cargar()
    if not tareas:
        console.print("[yellow]No hay tareas.[/yellow]")
        return
    tabla = Table(title="Mis tareas")
    tabla.add_column("#", justify="right")
    tabla.add_column("Tarea")
    tabla.add_column("Estado")
    for i, t in enumerate(tareas, start=1):
        estado = "[green]✔ hecha[/green]" if t["hecha"] else "[red]pendiente[/red]"
        tabla.add_row(str(i), t["texto"], estado)
    console.print(tabla)


def hecha(numero):
    tareas = cargar()
    if not 1 <= numero <= len(tareas):
        console.print("[red]Ese número no existe.[/red]")
        return
    tareas[numero - 1]["hecha"] = True
    guardar(tareas)
    console.print(f"[green]Completada:[/green] {tareas[numero - 1]['texto']}")


def borrar(numero):
    tareas = cargar()
    if not 1 <= numero <= len(tareas):
        console.print("[red]Ese número no existe.[/red]")
        return
    eliminada = tareas.pop(numero - 1)
    guardar(tareas)
    console.print(f"[yellow]Borrada:[/yellow] {eliminada['texto']}")


def main():
    parser = argparse.ArgumentParser(description="Gestor de tareas")
    sub = parser.add_subparsers(dest="comando", required=True)

    p_add = sub.add_parser("add", help="añadir una tarea")
    p_add.add_argument("texto")

    sub.add_parser("list", help="listar tareas")

    p_done = sub.add_parser("done", help="marcar como hecha")
    p_done.add_argument("numero", type=int)

    p_del = sub.add_parser("del", help="borrar una tarea")
    p_del.add_argument("numero", type=int)

    args = parser.parse_args()

    if args.comando == "add":
        anadir(args.texto)
    elif args.comando == "list":
        listar()
    elif args.comando == "done":
        hecha(args.numero)
    elif args.comando == "del":
        borrar(args.numero)


if __name__ == "__main__":
    main()