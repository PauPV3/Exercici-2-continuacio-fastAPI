document.addEventListener("DOMContentLoaded", function() {
    // Cridem a l'endpoint de l'API fent un fetch
    fetch('http://localhost:8000/alumne/listAll')  // Crida a l'API a l'endpoint
        .then(response => {
            if (!response.ok) {
                throw new Error("Error a la resposta del servidor");
            }
            return response.json();
        })
        .then(data => {
            const alumnesTableBody = document.querySelector("#tablaAlumne tbody");
            alumnesTableBody.innerHTML = ""; // Netejar la taula abans d'afegir res
            
            // Iterar sobre els alumnes i afegir-los al DOM
            data.forEach(alumne => {
                const row = document.createElement("tr");

                const nomAluCell = document.createElement("td");
                nomAluCell.textContent = alumne.NomAlumne;
                row.appendChild(nomAluCell);

                // Cicle
                const cicleCell = document.createElement("td");
                cicleCell.textContent = alumne.Cicle;
                row.appendChild(cicleCell);

                // Curs
                const cursCell = document.createElement("td");
                cursCell.textContent = alumne.Curs;
                row.appendChild(cursCell);

                // Grup
                const grupCell = document.createElement("td");
                grupCell.textContent = alumne.Grup;
                row.appendChild(grupCell);

                // Aula
                const descAulaCell = document.createElement("td");
                descAulaCell.textContent = alumne.DescAula;
                row.appendChild(descAulaCell);

                alumnesTableBody.appendChild(row);
            });
        })
        .catch(error => {
            console.error("Error capturat:", error);
            alert("Error al carregar la llista d'alumnes");
        });
});
