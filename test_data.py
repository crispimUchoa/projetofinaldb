from entities.Consulta import Consulta
from entities.Medicamento import Medicamento
from entities.Paciente import Paciente
from entities.Medico import Medico

pacientes = [
    Paciente(1, "Paciente 1", "senha1", "paciente1@exemplo.com", "Unimed", "Nenhuma", "(11) 912345678", '9999-92-01'),
    Paciente(2, "Paciente 2", "senha2", "paciente2@exemplo.com", "Bradesco Saúde", "Deficiência auditiva", "(11) 923456789", '9999-92-01'),
    Paciente(3, "Paciente 3", "senha3", "paciente3@exemplo.com", "Amil", "Nenhuma", "(11) 934567890", '9999-92-01'),
    Paciente(4, "Paciente 4", "senha4", "paciente4@exemplo.com", "Hapvida", "Deficiência visual", "(11) 945678901", '9999-92-01'),
    Paciente(5, "Paciente 5", "senha5", "paciente5@exemplo.com", "Unimed", "Mobilidade reduzida", "(11) 956789012", '9999-92-01'),
    Paciente(6, "Paciente 6", "senha6", "paciente6@exemplo.com", "Bradesco Saúde", "Nenhuma", "(11) 967890123", '9999-92-01'),
    Paciente(7, "Paciente 7", "senha7", "paciente7@exemplo.com", "Amil", "Deficiência auditiva", "(11) 978901234", '9999-92-01'),
    Paciente(8, "Paciente 8", "senha8", "paciente8@exemplo.com", "Hapvida", "Mobilidade reduzida", "(11) 989012345", '9999-92-01'),
    Paciente(9, "Paciente 9", "senha9", "paciente9@exemplo.com", "Unimed", "Nenhuma", "(11) 990123456", '9999-92-01'),
    Paciente(10, "Paciente 10", "senha10", "paciente10@exemplo.com", "Bradesco Saúde", "Deficiência visual", "(11) 901234567", '9999-92-01'),
]

medicos = [
    Medico(11, "Dr. Carlos Silva", "senha1", "dr.carlos@exemplo.com", "Cardiologia", ["08:00-12:00", "14:00-18:00"], 5, True),
    Medico(12, "Dra. Maria Oliveira", "senha2", "dra.maria@exemplo.com", "Pediatria", ["09:00-13:00", "15:00-19:00"], 7, False),
    Medico(13, "Dr. João Souza", "senha3", "dr.joao@exemplo.com", "Neurologia", ["07:00-11:00", "13:00-17:00"], 2, True),
    Medico(14, "Dra. Fernanda Costa", "senha4", "dra.fernanda@exemplo.com", "Ginecologia", ["08:00-12:00", "16:00-20:00"], 8, True),
    Medico(15, "Dr. Rafael Lima", "senha5", "dr.rafael@exemplo.com", "Ortopedia", ["10:00-14:00", "15:00-19:00"], 3, False),
    Medico(16, "Dra. Ana Pires", "senha6", "dra.ana@exemplo.com", "Dermatologia", ["08:00-12:00", "14:00-18:00"], 9, True),
    Medico(17, "Dr. Lucas Almeida", "senha7", "dr.lucas@exemplo.com", "Oftalmologia", ["09:00-13:00", "15:00-19:00"], 6, False),
    Medico(18, "Dra. Camila Rocha", "senha8", "dra.camila@exemplo.com", "Psiquiatria", ["08:00-12:00", "14:00-18:00"], 4, True),
    Medico(19, "Dr. Roberto Lima", "senha9", "dr.roberto@exemplo.com", "Urologia", ["07:00-11:00", "13:00-17:00"], 5, False),
    Medico(20, "Dra. Paula Martins", "senha10", "dra.paula@exemplo.com", "Endocrinologia", ["08:00-12:00", "15:00-19:00"], 7, True)
]


consultas = [
    Consulta(1, pacientes[0], medicos[0], "2025-02-15", 250.50, "Consulta de rotina 1", 4),
    Consulta(2, pacientes[1], medicos[1], "2025-02-18", 300.75, "Consulta de check-up", 5),
    Consulta(3, pacientes[2], medicos[2], "2025-02-20", 180.00, "Consulta dermatológica", 3),
    Consulta(4, pacientes[3], medicos[3], "2025-02-22", 400.00, "Consulta cardiológica", 5),
    Consulta(5, pacientes[4], medicos[4], "2025-02-25", 220.30, "Consulta pediátrica", 4),
    Consulta(6, pacientes[5], medicos[5], "2025-02-28", 320.00, "Consulta ortopédica", 5),
    Consulta(7, pacientes[6], medicos[6], "2025-03-03", 150.90, "Consulta ginecológica", 3),
    Consulta(8, pacientes[7], medicos[7], "2025-03-07", 275.60, "Consulta oftalmológica", 4),
    Consulta(9, pacientes[8], medicos[8], "2025-03-10", 290.80, "Consulta neurológica", 5),
    Consulta(10, pacientes[9], medicos[9], "2025-03-15", 210.50, "Consulta psiquiátrica", 4),
]

users = [*pacientes, *medicos]

medicamentos = [
    Medicamento("Paracetamol", "Laboratório A"),
    Medicamento("Ibuprofeno", "Laboratório B"),
    Medicamento("Amoxicilina", "Laboratório C"),
    Medicamento("Dipirona", "Laboratório D"),
    Medicamento("Omeprazol", "Laboratório E"),
    Medicamento("Losartana", "Laboratório F"),
    Medicamento("Loratadina", "Laboratório G"),
    Medicamento("Metformina", "Laboratório H"),
    Medicamento("Azitromicina", "Laboratório I"),
    Medicamento("Fluoxetina", "Laboratório J")
]
