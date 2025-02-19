pesquisaMedInput = document.getElementById('input-pesquisa-med')

pesquisaMedInput?.setSelectionRange(pesquisaMedInput.value.length, pesquisaMedInput.value.length)
pesquisaMedInput?.addEventListener('input', (ev)=>{
    document.getElementById('form-pesquisa-med').submit()
})

const stars = document.querySelectorAll(".stars i");
    let rating = 0;

    stars.forEach(star => {
        star.addEventListener("mouseover", function() {
            let value = this.getAttribute("data-value");
            highlightStars(value);
        });

        star.addEventListener("click", function() {
            rating = this.getAttribute("data-value");
            document.getElementById("rating").value = rating;
        });

        star.addEventListener("mouseleave", function() {
            highlightStars(rating);
        });
    });

    function highlightStars(value) {
        stars.forEach(star => {
            if (star.getAttribute("data-value") <= value) {
                star.classList.add("checked");
            } else {
                star.classList.remove("checked");
            }
        });
    }

    function enviarAvaliacao() {
        const nota = document.getElementById("rating").value;
        fetch("/avaliar_medico/{{ medico.id }}", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ nota: nota })
        }).then(response => response.json())
        .then(data => {
            alert(data.mensagem);
            document.getElementById("nota-media").innerText = data.nova_media;
        })
        .catch(error => console.error("Erro:", error));
        alert("Avaliação enviada com sucesso");
    }

document.getElementById("marcar-consulta-date").min = new Date().toISOString().slice(0, 16);

document.addEventListener("DOMContentLoaded", function () {
    document.querySelector(".btn-avaliar").addEventListener("click", function (event) {
        event.preventDefault(); // Impede o envio imediato do formulário

        let confirmacao = confirm("Tem certeza de que deseja enviar sua avaliação?");
        if (confirmacao) {
            enviarAvaliacao();
        }
    });
});

const botao = document.getElementById("marcar-consulta-btn");
    if (!botao) {
        console.error("Botão não encontrado!");
        return;
    }


    const form = document.querySelector(".marcar-consulta-form");
    const horariosOcupados = JSON.parse(form.getAttribute("data-horarios"));

    form.addEventListener("submit", function (event) {
        event.preventDefault();
        const inputDataHora = document.getElementById("marcar-consulta-date").value;
        if (horariosOcupados.includes(inputDataHora)) {
            alert("Este horário já está ocupado. Escolha outro.");

        }
    });
