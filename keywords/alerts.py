ALERTS = [
    # termos diretos de suicídio
    "matar", "me matar", "vou me matar", "quero me matar", "quero morrer", "não quero mais viver",
    "não quero mais", "acabar com tudo", "acabar com minha vida", "não aguento mais viver",
    "tô cansado de viver", "estou cansado de viver", "cansei de viver", "tirar minha vida",
    "me tirar a vida", "dar fim à minha vida", "dar fim em tudo", "acabar com isso",
    "suicidar", "suicídio", "suicidio", "me suicidar", "tentar me matar", "ideação suicida",
    "ideacao suicida", "ideacao", "me autoexterminar", "me suicido", "penso em morrer",
    "penso em me matar", "pensando em morrer", "pensando em me matar", "morrer logo",
    "queria morrer", "preferia morrer", "morrer é melhor", "melhor morrer", "vontade de morrer",
    "vontade de sumir", "queria sumir", "sumir pra sempre", "sumir do mapa", "deixar de existir",
    "não aguento", "não suporto mais", "não vejo saída", "sem saída", "sem esperança", "sem motivo",
    "sem razão pra viver", "cansado da vida", "desistir da vida", "cansei de tudo", "cansei de lutar",
    "m0rrer", "mort3", "m0rter", "ac@bar", "sucidar", "su!cidar", "suic1dio", "suic!dio",

    # automutilação
    "me cortar", "me cortei", "me cortando", "me machucar", "me machuco", "me ferir", "me ferindo",
    "me feri", "cortei o pulso", "cortar o pulso", "cortar os pulsos", "machucar o pulso",
    "sangrar", "sangrei", "auto mutilação", "automutilação", "automutilacao", "autolesão",
    "auto lesão", "autolesao", "auto ferimento", "auto ferir", "me bater", "me espancar",
    "quero sentir dor", "mereço sofrer", "quero sofrer", "me punir", "me punindo", "me castigando",
    "machucar a mim mesmo", "me destruir", "me acabando", "me machuquei", "ferir a mim mesmo",
    "c0rtar", "me c0rtar", "m4chucar", "auto-mutilar", "aut0lesao",

    # depressão profunda
    "depressão", "depressivo", "depressiva", "depressao", "sem vontade de viver", "sem forças",
    "sem energia pra nada", "sem ânimo", "sem sentido", "vida sem sentido", "nada faz sentido",
    "não tem mais jeito", "tudo acabou", "minha vida acabou", "não há mais esperança",
    "me sinto vazio", "me sinto inútil", "sou um fracasso", "sou inútil", "sou um peso",
    "peso pra todos", "ninguém se importa", "ninguém liga pra mim", "ninguém vai sentir falta",
    "ninguém me ama", "ninguém vai notar", "ninguém se importa comigo", "não faço falta",
    "cansei de tentar", "não consigo mais", "não tenho forças", "não aguento mais essa dor",
    "dor insuportável", "dor emocional", "dor na alma", "sofrimento constante", "não suporto",
    "quero dormir pra sempre", "queria dormir e não acordar", "queria apagar pra sempre",
    "queria sumir do mundo", "chega", "basta", "fim", "acabou tudo", "já era", "não tem mais volta",
    "sem sentido pra viver", "cansado de lutar", "exausto da vida", "vazio por dentro",
    "tô destruído", "estou destruído", "não tenho mais motivo", "tudo dói", "tudo é dor",

    # violência e atentados
    "atentado", "explosão", "bomba", "tiroteio", "massacre", "matança", "atirar", "fuzilar",
    "explodir", "planejar atentado", "planejando atentado", "ataque", "assassinar", "assassinato",
    "matar pessoas", "matar todos", "vou matar alguém", "vou matar todo mundo", "planejar massacre",
    "tiro na cabeça", "tiros", "facada", "bala", "arma", "arma de fogo", "carregar arma",
    "preparar bomba", "explosivo", "explodir tudo", "escola atentado", "atacar", "morte em massa",
    "genocídio", "terrorismo", "terrorista", "ameaçar matar", "vontade de matar", "pessoa vai morrer",
    "fazer justiça com as próprias mãos", "vontade de atirar", "sangue", "mass@cre", "b0mba", "t!roteio",

    # morte e desespero
    "morrer", "morreu", "morte", "morto", "falecer", "falecimento", "descansar em paz",
    "descansar pra sempre", "quero partir", "partir dessa", "não volto mais", "sem volta",
    "ponto final", "acabar de vez", "dar adeus", "adeus", "última mensagem", "me despedindo",
    "me despedir", "não quero mais continuar", "hora de ir", "chegou minha hora",
    "minha última hora", "não quero mais sentir nada", "nada mais importa", "tudo acabou",
    "fim da linha", "fim pra mim", "tô no fim", "quero ir embora", "morrer dormindo",
    "descansar de vez", "encerrar tudo", "final de tudo", "último dia", "último adeus",
    "quero desistir", "vou desistir", "não dá mais pra mim", "não quero mais lutar",
    "sem perspectiva", "sem solução", "sem importância", "sem saída", "acabou pra mim",
    "morrendo por dentro", "morrendo aos poucos", "morrendo devagar",

    # termos de risco iminente
    "vou fazer uma besteira", "vou fazer algo ruim", "vou fazer uma loucura", "vou sumir",
    "ninguém vai me achar", "ninguém vai notar", "não volto mais", "não aguento mais isso",
    "acho que chegou minha hora", "já decidi", "está decidido", "não quero mais lutar",
    "não quero mais sentir nada", "tudo dói demais", "nada mais importa", "sem importância",
    "sem perspectiva", "sem solução", "chega de sofrimento", "sofri demais", "já sofri o bastante",
    "não quero mais sofrer", "não tem motivo pra continuar", "não consigo ver futuro",
    "tô indo embora", "adeus pra sempre", "me despedindo de todos", "chegou ao fim",
    "último recado", "último texto", "última vez que escrevo",

    # termos em inglês
    "kill myself", "want to die", "i want to die", "i dont want to live", "i don't want to live",
    "i cant go on", "i can't go on", "i give up", "no reason to live", "i'm done", "im done",
    "life is over", "end my life", "end it all", "suicide", "suicidal", "self harm",
    "cut myself", "hurt myself", "cant take it anymore", "can't take it anymore", "die soon",
    "wish i was dead", "wish i could die", "hope i die", "ready to die", "kill me please",
    "tired of life", "life is pointless", "nothing matters", "want to disappear", "dont care anymore",
    "life over", "death", "dying", "kill them all", "bomb", "attack", "shoot", "school shooting",
    "gun", "mass shooting", "terror attack", "explode", "explode myself", "end everything",

    # formas cifradas e slangs online
    "m0rrer", "m0rre", "m0rto", "m0rri", "su!cidar", "su!cida", "suic!dio", "m0rt3", "m0rt", "m0rti",
    "acab4r", "m@tar", "m@to", "m@t4r", "m@t4ndo", "t0 cansado", "sum!r", "sumi@", "desc@nsar",
    "d0r", "t0 desistindo", "adeu$", "fim d3 tud0", "acab0u", "acab0", "at3ntado", "at3nt@do",
    "b0mb@", "explo$ão", "explo$ivo", "t!roteio", "t1r0", "suf0cado", "enforcar", "me enforcar",
    "me afogar", "afogamento", "me jogar", "pular da ponte", "pular do prédio", "se jogar", "tomar remédio",
    "tomar remedio demais", "overdose", "tomar veneno", "veneno", "remédio demais", "remedio demais"
]
