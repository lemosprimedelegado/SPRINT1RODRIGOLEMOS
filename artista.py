class Artista:
    def __init__(self, nome, genero, data_nascimento, contacto, discografia):
        self.id = None
        self.nome = nome
        self.gênero = genero
        self.data_nascimento = data_nascimento  # Correct attribute name
        self.contacto = contacto
        self.discografia = discografia

    def __str__(self):
        return f"{self.nome};{self.gênero};{self.data_nascimento};{self.contacto};{self.discografia}"  # Use data_nascimento

    @classmethod
    def from_string(cls, data_str):
        try:
            nome, genero, data_nascimento, contacto, discografia = data_str.strip().split(';')
            return cls(nome, genero, data_nascimento, contacto, discografia)  # Use data_nascimento
        except ValueError:
            print(f"Erro ao ler linha: '{data_str}'. Formato esperado: 'nome;gênero;data_nascimento;contacto;discografia'")
            return None
