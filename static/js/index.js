pesquisaMedInput = document.getElementById('input-pesquisa-med')

pesquisaMedInput?.setSelectionRange(pesquisaMedInput.value.length, pesquisaMedInput.value.length)
pesquisaMedInput?.addEventListener('input', (ev)=>{
    document.getElementById('form-pesquisa-med').submit()
})

