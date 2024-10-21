from db_alumnat import get_db_connection
from fastapi import HTTPException

def list_all_alumnes():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT alumne.NomAlumne, alumne.Cicle, alumne.Curs, alumne.Grup, aula.DescAula
        FROM alumne
        JOIN aula ON alumne.IdAula = aula.IdAula
    """)
    alumnes = cursor.fetchall()
    conn.close()
    return alumnes

def query_alumnes(orderby: str = None, contain: str = None, skip: int = 0, limit: int = None):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT alumne.NomAlumne, alumne.Cicle, alumne.Curs, alumne.Grup, aula.DescAula
        FROM alumne
        JOIN aula ON alumne.IdAula = aula.IdAula
    """
    conditions = []

    if contain:
        conditions.append(f"alumne.NomAlumne LIKE '%{contain}%'")

    if orderby in ['asc', 'desc']:
        query += f" ORDER BY alumne.NomAlumne {orderby}"

    if skip or limit:
        query += f" LIMIT {limit or 100} OFFSET {skip or 0}"

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    cursor.execute(query)
    alumnes = cursor.fetchall()
    conn.close()
    return alumnes

def insert_alumne_from_csv(nomAlumne, cicle, curs, grup, descAula, edifici, pis):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM aula WHERE DescAula = %s", (descAula,))
    aula = cursor.fetchone()
    if not aula:
        cursor.execute("INSERT INTO aula (DescAula, Edifici, Pis) VALUES (%s, %s, %s)", (descAula, edifici, pis))
        conn.commit()
        aula_id = cursor.lastrowid
    else:
        aula_id = aula['IdAula']

    cursor.execute("""
        INSERT INTO alumne (NomAlumne, Cicle, Curs, Grup, IdAula)
        VALUES (%s, %s, %s, %s, %s)
    """, (nomAlumne, cicle, curs, grup, aula_id))
    conn.commit()
    conn.close()
