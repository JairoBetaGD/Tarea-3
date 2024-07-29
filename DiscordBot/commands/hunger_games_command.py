import discord
import random
import asyncio
from discord import File
from discord.embeds import Embed
from commands.command_base import Command, send_message

class HungerGamesCommand(Command):
    async def execute(self):

        event_round_chance = 0.45  # Probabilidad de una ronda de evento (45%)
        elimination_chance_normal = 0.25  # Probabilidad de eliminación en rondas normales (25%)
        elimination_chance_event = 0.55  # Probabilidad de eliminación en rondas de evento (55%)


        rounds = 0

        # Verificar si el autor del mensaje tiene el rol permitido
        allowed_role_name = "Ω★★★ ADMINISTRACIÓN ★★★Ω"  # Reemplaza con el nombre del rol
        allowed_role = discord.utils.get(self.message.guild.roles, name=allowed_role_name)

        if allowed_role not in self.message.author.roles:
            await send_message(self.message.channel, f"No tienes permiso para usar este comando.")
            return

        # Obtener las menciones de los participantes desde el mensaje
        mentions = self.message.mentions

        print(len(mentions))
        # Verificar si hay suficientes participantes
        if len(mentions) < 32:
            await send_message(self.message.channel, "No hay suficientes participantes para iniciar el juego (deben ser al menos 32).")
            return

        participants = mentions  # Usar las menciones como participantes


        # Lista de mensajes normales
        normal_messages = [
            "{usuario} ha afilado sus cuchillos.",
            "{usuario} está buscando agua.",
            "{usuario} se ha aliado con {usuario1}.",
            "{usuario} está escondido en un árbol.",
            "{usuario} ha encontrado una bolsa de provisiones.",
            "{usuario} ha construido un refugio.",
            "{usuario} está siguiendo las huellas de {usuario1}.",
            "{usuario} ha perdido su camino.",
            "{usuario} ha encontrado una trampa mortal.",
            "{usuario} está cazando para conseguir comida.",
            "{usuario} ha recibido un regalo de un patrocinador.",
            "{usuario} está planeando su próximo movimiento.",
            "{usuario} se ha topado con una manada de mutantes.",
            "{usuario} ha formado una alianza temporal con {usuario1}.",
            "{usuario} ha encontrado una fuente de agua potable.",
            "{usuario} está desesperado por comida.",
            "{usuario} está construyendo una trampa.",
            "{usuario} está escondido en una cueva.",
            "{usuario} se ha lesionado.",
            "{usuario} ha perdido su equipo.",
            "{usuario} ha descubierto una pista misteriosa.",
            "{usuario} está escalando un árbol alto.",
            "{usuario} está cazando insectos para comer.",
            "{usuario} está tratando de encender una fogata.",
            "{usuario} ha encontrado una señal en el cielo.",
            "{usuario} está siguiendo el rastro de {usuario1}.",
            "{usuario} está nadando en un río peligroso.",
            "{usuario} ha caído en una trampa.",
            "{usuario} ha recibido una herida grave.",
            "{usuario} está construyendo un refugio fortificado.",
            "{usuario} está cazando aves para obtener comida.",
            "{usuario} ha encontrado un arco y flechas.",
            "{usuario} está tratando de comunicarse con otros tributos.",
            "{usuario} ha recibido una cura de sus patrocinadores.",
            "{usuario} ha descubierto una entrada secreta a una cueva.",
            "{usuario} ha perdido su brújula y está perdido.",
            "{usuario} está escalando una montaña escarpada.",
            "{usuario} está cazando peces en el río.",
            "{usuario} ha construido una balsa improvisada.",
            "{usuario} ha descubierto un escondite de suministros.",
            "{usuario} está ocultando una lesión para no mostrar debilidad.",
            "{usuario} y {usuario1} se han aliado para sobrevivir juntos.",
            "{usuario} y {usuario1} han comenzado una pelea por comida.",
            "{usuario} encontró un escondite seguro mientras {usuario1} sigue buscando refugio.",
            "{usuario1} logró atrapar a un conejo para alimentarse, mientras {usuario} observaba con envidia.",
            "{usuario} y {usuario1} se han separado en busca de suministros, esperemos que se reencuentren pronto.",
            "{usuario} besa a {usuario1}",
        ]

        elimination_messages = [
            "{usuario1} apuñaló 30 veces a {usuario}.",
            "{usuario1} superó a {usuario} en un feroz enfrentamiento.",
            "{usuario1} no tuvo piedad y eliminó a {usuario} sin problemas.",
            "{usuario} no superó las circunstancias y se suicidó.",
            "{usuario1} cazó a {usuario} como una presa fácil.",
            "{usuario1} acabó con la vida de {usuario} con una trampa mortal.",
            "{usuario1} emboscó a {usuario} y lo dejó sin oportunidad de escapar.",
            "{usuario1} encontró a {usuario} y lo eliminó en un enfrentamiento mortal.",
            "{usuario} fue sorprendido por {usuario1} y no pudo defenderse.",
            "{usuario1} acechó a {usuario} durante horas antes de matarlo.",
            "{usuario1} se cruzó en el camino de {usuario} y no lo dejó con vida.",
            "{usuario1} se enfrentó valientemente a {usuario} y lo mató en una pelea justa.",
            "{usuario1} atacó a {usuario} mientras dormía, acabando con su vida.",
            "{usuario} intentó escapar, pero {usuario1} lo atrapó y lo mató sin piedad.",
            "{usuario} intentó formar una alianza, pero {usuario1} lo traicionó y lo mató.",
            "{usuario1} cazó a {usuario} como una presa y lo mató sin compasión.",
            "{usuario1} sorprendió a {usuario} mientras buscaba refugio y lo mató sigilosamente.",
            "{usuario1} ideó un astuto plan para eliminar a {usuario} y lo ejecutó con precisión.",
            "{usuario} y {usuario1} se encontraron cara a cara, pero solo uno sobrevivió, y fue {usuario1}.",
            "{usuario} intentó resistirse, pero la determinación de {usuario1} fue inquebrantable, y lo mató.",
            "{usuario} murió de hambre",
            "{usuario} luchó valientemente, pero finalmente cayó ante las adversidades.",
            "{usuario} se quedó sin recursos y no pudo seguir adelante.",
            "{usuario} hizo su último intento, pero la suerte no estuvo de su lado.",
            "{usuario} enfrentó su destino con valentía, pero no logró sobrevivir.",
            "{usuario} fue atrapado en una tormenta salvaje y no pudo encontrar refugio a tiempo.",
            "La naturaleza implacable reclamó a {usuario}, quien no pudo sobrevivir a las adversidades del bosque.",
            "{usuario} se encontró con un río furioso y no pudo cruzarlo con seguridad.",
            "{usuario} cayó en una trampa natural mientras exploraba el terreno y no pudo liberarse a tiempo.",
            "Los depredadores de la naturaleza acecharon a {usuario}, quien no pudo evitar convertirse en presa.",
            "{usuario} no pudo soportar el salario mínimo venezolano y murió de hambre",
        ]

        gas_normal_messages = [
            "{usuario} lucha por encontrar aire limpio mientras el gas venenoso se acerca.",
            "{usuario} busca desesperadamente una máscara de gas para sobrevivir al evento.",
            "{usuario} se refugia en una cueva, tratando de evitar el gas venenoso.",
            "{usuario} intenta trepar a un árbol para escapar del gas tóxico.",
            "{usuario} se encuentra con una fuente de agua, pero teme que esté contaminada por el gas venenoso.",
            "{usuario} se tambalea mientras el gas venenoso afecta su visión y respiración.",
            "{usuario} busca en sus provisiones una solución para protegerse del gas venenoso.",
            "{usuario} tose violentamente mientras el gas venenoso se cierne a su alrededor.",
            "{usuario} se desliza por el suelo, tratando de encontrar una salida del gas tóxico.",
            "{usuario} busca frenéticamente una máscara de gas entre los escombros.",
            "{usuario} comparte su máscara de gas con {usuario1}, demostrando lealtad en medio del peligro.",
            "{usuario} se tambalea, sintiéndose mareado por la exposición al gas venenoso.",
            "{usuario} escucha los débiles sollozos de otros tributos atrapados en el gas venenoso.",
            "{usuario} se refugia en una pequeña grieta de la roca para escapar del gas tóxico.",
            "{usuario} comparte sus últimas provisiones de oxígeno con {usuario1} en un gesto desinteresado.",
            "{usuario} encuentra un rincón aparentemente seguro, pero el gas venenoso se acerca rápidamente.",
            "{usuario} usa una tela mojada para filtrar el aire mientras lucha contra el gas tóxico.",
            "{usuario} intenta comunicarse con otros tributos a través de un walkie-talkie, buscando aliados para enfrentar el gas venenoso.",
            "{usuario} y {usuario1} trabajan juntos para sellar una puerta y evitar que el gas venenoso entre en su refugio.",
        ]

        gas_elimination_messages = [
            "{usuario1} atrapa a {usuario} mientras luchaban por una máscara de gas, acabando con su vida.",
            "{usuario1} embosca a {usuario} en la densa nube de gas venenoso y lo elimina.",
            "{usuario1} encuentra a {usuario} debilitado por el gas venenoso y lo remata sin piedad.",
            "{usuario} intenta escapar del gas venenoso, pero {usuario1} lo sigue y lo elimina.",
            "{usuario} se desmaya debido al gas venenoso y {usuario1} lo elimina mientras está indefenso.",
            "{usuario1} se protege adecuadamente del gas venenoso y sorprende a {usuario} desprevenido.",
            "{usuario} lucha por respirar mientras {usuario1} lo elimina sin misericordia en medio del gas venenoso.",
            "{usuario} se derrumba, víctima del gas venenoso que finalmente lo alcanzó.",
            "{usuario1} observa impotente mientras el gas tóxico se lleva a {usuario}.",
            "El gas venenoso envuelve a {usuario} en su abrazo mortal, dejando solo silencio.",
            "{usuario} intenta huir del gas venenoso, pero sus esfuerzos son en vano.",
            "{usuario} cae al suelo, tosiendo sangre debido al gas venenoso.",
            "{usuario} se desvanece lentamente mientras el gas tóxico lo envuelve por completo.",
            "{usuario} se ahoga en el gas venenoso, luchando por su última bocanada de aire.",
            "{usuario} no pudo encontrar refugio y ahora es presa del gas venenoso.",
            "{usuario} se despide de este mundo, atrapado en la nube mortal del gas tóxico.",
            "{usuario} intenta resistir, pero el gas venenoso es implacable en su búsqueda.",
            "{usuario1} ve cómo {usuario} colapsa, incapaz de salvarlo del gas venenoso.",
            "La traicionera naturaleza del gas venenoso reclama a {usuario}, dejando un triste recordatorio.",
        ]

        volcano_normal_messages = [
            "{usuario} siente el suelo temblar bajo sus pies mientras el volcán entra en erupción.",
            "{usuario} corre para resguardarse de la lluvia de ceniza y rocas lanzada por el volcán.",
            "{usuario} escucha el estruendo del volcán y se apresura a buscar refugio.",
            "{usuario} se cubre la boca y la nariz con un pañuelo para protegerse de la ceniza volcánica.",
            "{usuario} lucha por mantener el equilibrio mientras el terreno se sacude debido a la erupción.",
            "{usuario} observa cómo una corriente de lava fluye por el paisaje, bloqueando su camino.",
            "{usuario} se adentra en una cueva para escapar de la lluvia de ceniza y la roca ardiente.",
            "{usuario} intenta apagar un incendio provocado por la erupción antes de que se propague.",
            "{usuario} busca agua para enfriar su piel quemada por la ceniza volcánica.",
            "{usuario} se refugia en un refugio improvisado mientras la erupción continúa.",
            "{usuario} se desliza peligrosamente por una ladera cubierta de ceniza volcánica.",
            "{usuario} encuentra un arco y flechas en medio del caos de la erupción.",
            "{usuario} se apresura a ayudar a otros tributos a llegar a un lugar seguro.",
            "{usuario} observa cómo un árbol cercano se incendia debido a la erupción.",
            "{usuario} se refugia en una grieta del terreno para escapar de la lava ardiente.",
            "{usuario} y {usuario1} sienten el suelo temblar bajo sus pies mientras el volcán entra en erupción.",
            "{usuario} y {usuario1} corren para resguardarse de la lluvia de ceniza y rocas lanzada por el volcán.",
            "{usuario} y {usuario1} escuchan el estruendo del volcán y se apresuran a buscar refugio juntos.",
            "{usuario} y {usuario1} se cubren la boca y la nariz con un pañuelo para protegerse de la ceniza volcánica.",
            "{usuario} y {usuario1} luchan por mantener el equilibrio mientras el terreno se sacude debido a la erupción.",
            "{usuario} y {usuario1} observan cómo una corriente de lava fluye por el paisaje, bloqueando su camino.",
            "{usuario} y {usuario1} se adentran en una cueva para escapar de la lluvia de ceniza y la roca ardiente juntos.",
            "{usuario} y {usuario1} intentan apagar un incendio provocado por la erupción antes de que se propague.",
            "{usuario} y {usuario1} buscan agua juntos para enfriar sus pieles quemadas por la ceniza volcánica.",
            "{usuario} y {usuario1} se refugian en un refugio improvisado mientras la erupción continúa a su alrededor.",
        ]

        volcano_elimination_messages = [
            "{usuario1} atrapa a {usuario} en una avalancha de ceniza volcánica y lo mata.",
            "{usuario} intenta escapar de la lava, pero {usuario1} lo alcanza y lo elimina en el proceso.",
            "{usuario1} cierra la entrada de la cueva en la que se encuentra {usuario}, atrapándolo en una tumba de lava.",
            "{usuario} lucha por mantenerse en pie mientras {usuario1} aprovecha la erupción para eliminarlo.",
            "{usuario1} bloquea el camino de {usuario} y lo arroja a la corriente de lava.",
            "{usuario} cae en una trampa de ceniza volcánica preparada por {usuario1} y queda eliminado.",
            "{usuario1} se enfrenta valientemente a {usuario} en medio de la erupción y lo elimina en un enfrentamiento feroz.",
            "{usuario} se desvía del camino debido a la erupción y {usuario1} lo embosca, matándolo.",
            "{usuario1} usa la confusión causada por la erupción para atacar a {usuario} y dejarlo sin oportunidad de escape.",
            "{usuario} cae en una grieta del terreno mientras trata de escapar, y {usuario1} lo mata sin piedad.",
            "{usuario1} utiliza la lava ardiente para eliminar a {usuario} de manera brutal.",
            "{usuario} intenta huir escalando una ladera, pero {usuario1} lo derriba y lo mata.",
            "{usuario1} bloquea la única salida de {usuario} en una cueva y lo deja atrapado en el flujo de lava.",
            "{usuario} queda atrapado en un incendio provocado por la erupción, y {usuario1} lo asesina.",
            "{usuario1} observa con satisfacción mientras {usuario} se ahoga en una corriente de ceniza volcánica.",
            "{usuario} no pudo escapar a tiempo de la lluvia de lava y fue consumido por las llamas.",
            "{usuario} se deslizó por la pendiente volcánica y no pudo detenerse antes de caer en la lava ardiente.",
            "En su intento de escapar, {usuario} quedó atrapado en una nube de ceniza volcánica y no pudo respirar.",
            "{usuario} fue alcanzado por una roca ardiente lanzada por el volcán, poniendo fin a su vida.",
            "La erupción volcánica sorprendió a {usuario}, quien no tuvo oportunidad de huir.",
            "{usuario} quedó atrapado en una cueva colapsada debido a la erupción y no pudo sobrevivir.",
            "{usuario} luchó valientemente contra los elementos, pero la erupción fue implacable y lo mató.",
            "Una corriente de lava se cruzó en el camino de {usuario}, quien no pudo evitar su destino.",
            "{usuario} intentó escalar una pared de roca para escapar, pero perdió el agarre y cayó en la lava.",
            "A pesar de sus esfuerzos, {usuario} no pudo encontrar un refugio seguro de la erupción y fue consumido por el fuego.",
        ]

        wolfattack_normal_messages = [
            "¡{usuario} se une a la patrulla en busca de rastros de lobos!",
            "Los aullidos aterradores de los lobos llenan el aire, pero {usuario} mantiene la calma.",
            "una manada de lobos ataca a {usuario} pero asesina brutalmente a varios de ellos.",
            "Los lobos parecen estar estudiando a {usuario} desde la oscuridad.",
            "La noche está llena de tensión mientras {usuario} y los aldeanos aguardan el próximo movimiento de los lobos.",
            "El miedo es palpable, pero la determinación de {usuario} no flaquea.",
            "Los lobos intentan un ataque sorpresa, pero son repelidos por la valentía de {usuario}.",
            "¡{usuario} y {usuario1} están en guardia, vigilando los movimientos de la manada de lobos!",
            "Los lobos se acercan sigilosamente a {usuario} y {usuario1}, pero logran espantarlos con antorchas.",
            "La valentía de {usuario1} y {usuario} es evidente mientras lideran la defensa contra los lobos.",
            "Una manada de lobos se congrega alrededor de {usuario1} y {usuario}, pero se retiran momentáneamente.",
            "{usuario} se comunica con {usuario1} para coordinar la defensa de la aldea contra los lobos.",
            "{usuario} logra escapar de los lobos mientras {usuario1} dispara flechas a varios de ellos",
            "los lobos caen en la trampa de {usuario1}"
        ]
       
        wolfattack_elimination_messages = [
            "{usuario} es emboscado por una manada de lobos y lucha valientemente, pero no logra sobrevivir.",
            "A pesar del coraje de {usuario}, los lobos lo superan en número y lo eliminan.",
            "Trágicamente, {usuario} no logra resistir el feroz ataque de los lobos.",
            "Los lobos rodean a {usuario}, quien lucha con valentía, pero cae ante la manada.",
            "La aldea lamenta la pérdida de {usuario}, quien cae víctima de los feroces lobos.",
            "{usuario} desaparece en la oscuridad del bosque, siendo víctima de un ataque sorpresa de lobos.",
            "A pesar de su valentía, {usuario} no puede resistir el embate de la manada de lobos.",
            "La manada de lobos se lleva a {usuario}, a pesar de su valiente resistencia.",
            "Los lobos acechan a {usuario} mientras intenta proteger a {usuario1}, pero desgraciadamente, no logra sobrevivir.",
            "Los lobos se abalanzan sobre {usuario}, cobrando su vida, pero {usuario1} logra escapar de su ataque.",
            "{usuario1} realiza un movimiento desesperado y empuja a los lobos hacia {usuario}, quien resulta ser su infortunada víctima.",
            "{usuario} es atacado por varios lobos mientras {usuario1} lo ve con desesperación",
            "{usuario} asesinado por {usuario1} quien lo usa como distracción",
        ]


        
        # Crear grupos de 4 participantes cada uno (tributos)
        tributos = [participants[i:i + 4] for i in range(0, len(participants), 4)]

        # Crear un embed para mostrar los tributos
        tributos_embed = Embed(title=f"Tributos", description="Aquí están los tributos para los Hunger Games:")

        for i, tributo_group in enumerate(tributos, start=1):
            group_text = "\n".join([f"{index + 1}. {member.mention}" for index, member in enumerate(tributo_group)])
            tributos_embed.add_field(name=f"Tributo {i}", value=group_text, inline=False)

        message = await self.message.channel.send(embed=tributos_embed)


        # URL de la imagen para las eliminaciones
        elimination_image_url = "https://img.freepik.com/fotos-premium/relampago-cementerio_337384-3050.jpg"

        # URL de la imagen para los mensajes normales
        normal_image_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRwRJBXlE87d8Css02rV9ORrh5sk2kO0AsRvA&usqp=CAU"

        await self.message.channel.send("Los Hunger Games empiezan en 30 segundos")
        await asyncio.sleep(30)

        while len(participants) > 1:
            rounds += 1
            await send_message(self.message.channel, f"**Dia {rounds}**")

            num_messages = 16
            is_event_round = rounds == 3 and len(participants) >= 16 and random.random() < event_round_chance
            if is_event_round:
                # random.randint(1,3)
                random_event = random.randint(1,3)

                if random_event == 1:
                    #Evento Gas Venenoso
                    gas_embed = Embed(
                        title="un Gas Venenoso mortal se apodera de la arena",
                        color=discord.Color.yellow()  # Puedes ajustar el color como prefieras
                    )

                    # Puedes agregar una imagen relacionada con el gas venenoso si lo deseas
                    gas_embed.set_image(url="https://thumbs.dreamstime.com/b/gas-venenoso-en-el-paisaje-de-pantano-surrealista-un-ai-generador-desastres-naturales-esta-ilustraci%C3%B3n-stock-muestra-con-270325256.jpg?w=360")

                    # Envía el embed al canal
                    await self.message.channel.send(embed=gas_embed)

                    await asyncio.sleep(10) #Esperar 10 segundos

                    while num_messages > 1:
                        if len(participants) == 1:
                            num_messages = 1
                        else:
                            if random.random() < elimination_chance_event:
                                eliminated = random.choice(participants)
                                participants.remove(eliminated)
                                    
                                # Seleccionar un mensaje de eliminación aleatorio de evento de gas venenoso
                                elimination_message = random.choice(gas_elimination_messages)
                                    
                                # Reemplazar {usuario1} y {usuario} con los nombres de usuario mencionados
                                elimination_message = elimination_message.replace("{usuario1}", random.choice(participants).mention)
                                elimination_message = elimination_message.replace("{usuario}", eliminated.mention)
                                    
                                # Generar un embed con el mensaje de eliminación y la imagen
                                embed = Embed(title="Eliminación - Gas Venenoso", description=elimination_message)
                                embed.set_image(url=elimination_image_url)
                                    
                                await self.message.channel.send(f"{eliminated.mention} ha sido eliminado")
                                await self.message.channel.send(embed=embed)
                                num_messages -= 1
                            else:
                                #Seleccionar mensaje aleatorio de evento de gas venenoso
                                normal_message = random.choice(gas_normal_messages)

                                #Reemplazar {usuario1} y {usuario} con los nombres de usuario mencionados
                                normal_message = normal_message.replace("{usuario}", random.choice(participants).mention)
                                normal_message = normal_message.replace("{usuario1}", random.choice(participants).mention)
                                
                                # Generar un embed para el mensaje normal con la imagen
                                embed = Embed(title=f"**Dia {rounds}** - Gas Venenoso", description=normal_message)
                                embed.set_image(url=normal_image_url)
                                
                                await self.message.channel.send(embed=embed)
                                num_messages -= 1

                        await asyncio.sleep(10)  # Esperar 10 segundos entre mensajes

                    gas_end_embed = Embed(
                        title="El gas se ha disipado, los participantes pueden estar más seguros",
                        color=discord.Color.green()  # Puedes ajustar el color como prefieras
                    )

                    # Envía el embed al canal
                    await self.message.channel.send(embed=gas_end_embed)



                elif random_event == 2:
                    #Evento Volcán en erupción
                    volcano_embed = Embed(
                        title="Cuidado. Un volcán ha entrado en erupción",
                        color=discord.Color.yellow()  # Puedes ajustar el color como prefieras
                    )

                    # Puedes agregar una imagen relacionada con el gas venenoso si lo deseas
                    volcano_embed.set_image(url="https://fotografias.lasexta.com/clipping/cmsimages02/2023/07/12/AD4AAF97-E8A3-4E71-8519-37692C8AB702/impactantes-imagenes-erupcion-volcan-islandia_98.jpg?crop=1254,706,x0,y65&width=1900&height=1069&optimize=high&format=webply")

                    # Envía el embed al canal
                    await self.message.channel.send(embed=volcano_embed)

                    await asyncio.sleep(10) #Esperar 10 segundos

                    while num_messages > 1:
                        if len(participants) == 1:
                            num_messages = 1
                        else:
                            if random.random() < elimination_chance_event:
                                eliminated = random.choice(participants)
                                participants.remove(eliminated)
                                    
                                # Seleccionar un mensaje de eliminación aleatorio de evento de gas venenoso
                                elimination_message = random.choice(volcano_elimination_messages)
                                    
                                # Reemplazar {usuario1} y {usuario} con los nombres de usuario mencionados
                                elimination_message = elimination_message.replace("{usuario1}", random.choice(participants).mention)
                                elimination_message = elimination_message.replace("{usuario}", eliminated.mention)
                                    
                                # Generar un embed con el mensaje de eliminación y la imagen
                                embed = Embed(title="Eliminación - Volcán en erupción", description=elimination_message)
                                embed.set_image(url=elimination_image_url)
                                    
                                await self.message.channel.send(f"{eliminated.mention} ha sido eliminado")
                                await self.message.channel.send(embed=embed)
                                num_messages -= 1
                            else:
                                #Seleccionar mensaje aleatorio de evento de gas venenoso
                                normal_message = random.choice(volcano_normal_messages)

                                #Reemplazar {usuario1} y {usuario} con los nombres de usuario mencionados
                                normal_message = normal_message.replace("{usuario}", random.choice(participants).mention)
                                normal_message = normal_message.replace("{usuario1}", random.choice(participants).mention)
                                
                                # Generar un embed para el mensaje normal con la imagen
                                embed = Embed(title=f"**Dia {rounds}** - Volcán en erupción", description=normal_message)
                                embed.set_image(url=normal_image_url)
                                
                                await self.message.channel.send(embed=embed)
                                num_messages -= 1

                        await asyncio.sleep(10)  # Esperar 10 segundos entre mensajes

                    volcano_end_embed = Embed(
                        title="La lava se ha secado y el volcán se ha calmado, ya queden ir más seguros",
                        color=discord.Color.green()  # Puedes ajustar el color como prefieras
                    )
                    await self.message.channel.send(embed=volcano_end_embed)
                

                elif random_event == 3:
                    wolf_embed = Embed(
                        title="Atención! una manada de lobos se acerca",
                        color=discord.Color.yellow()  # Puedes ajustar el color como prefieras
                    )
                    wolf_embed.set_image(url="https://i.pinimg.com/1200x/66/8b/94/668b94c3f32ea43abbd35c78432e7c7d.jpg")
                    
                    await self.message.channel.send(embed=wolf_embed)

                    await asyncio.sleep(10)

                    while num_messages > 1:
                        if len(participants) == 1:
                            num_messages = 1
                        else:
                            if random.random() < elimination_chance_event:
                                eliminated = random.choice(participants)
                                participants.remove(eliminated)

                                # Seleccionar un mensaje de ataque de lobos aleatorio
                                wolf_attack_message = random.choice(wolfattack_elimination_messages)

                                # Reemplazar {usuario1} y {usuario} con los nombres de usuario mencionados
                                wolf_attack_message = wolf_attack_message.replace("{usuario1}", random.choice(participants).mention)
                                wolf_attack_message = wolf_attack_message.replace("{usuario}", eliminated.mention)

                                # Generar un embed con el mensaje de eliminación y una imagen relacionada
                                embed = Embed(title="Eliminación - Ataque de Lobos", description=wolf_attack_message)
                                embed.set_image(url=elimination_image_url)

                                await self.message.channel.send(f"{eliminated.mention} ha sido eliminado")
                                await self.message.channel.send(embed=embed)
                                num_messages -= 1
                            else:
                                # Seleccionar un mensaje aleatorio para el evento de ataque de lobos
                                wolf_normal_message = random.choice(wolfattack_normal_messages)

                                # Reemplazar {usuario1} y {usuario} con los nombres de usuario mencionados
                                wolf_normal_message = wolf_normal_message.replace("{usuario}", random.choice(participants).mention)
                                wolf_normal_message = wolf_normal_message.replace("{usuario1}", random.choice(participants).mention)

                                # Generar un embed para el mensaje normal con una imagen
                                embed = Embed(title=f"**Dia {rounds}** - Ataque de Lobos", description=wolf_normal_message)
                                embed.set_image(url=normal_image_url)

                                await self.message.channel.send(embed=embed)
                                num_messages -= 1

                        await asyncio.sleep(10)  # Esperar 10 segundos entre mensajes
                    wolf_end_embed = Embed(
                        title="La manada de lobos se ha ido, ya pueden ir tranquilos",
                        color=discord.Color.green()  # Puedes ajustar el color como prefieras
                    )

                    await self.message.channel.send(embed=wolf_end_embed)



            else:
                #normal
                while num_messages > 1:
                    if len(participants) == 1:
                        num_messages = 1
                    else:
                        if random.random() < elimination_chance_normal:
                            eliminated = random.choice(participants)
                            participants.remove(eliminated)
                                
                            # Seleccionar un mensaje de eliminación aleatorio
                            elimination_message = random.choice(elimination_messages)
                                
                            # Reemplazar {usuario1} y {usuario} con los nombres de usuario mencionados
                            elimination_message = elimination_message.replace("{usuario1}", random.choice(participants).mention)
                            elimination_message = elimination_message.replace("{usuario}", eliminated.mention)
                                
                            # Generar un embed con el mensaje de eliminación y la imagen
                            embed = Embed(title="Eliminación", description=elimination_message)
                            embed.set_image(url=elimination_image_url)
                                
                            await self.message.channel.send(f"{eliminated.mention} ha sido eliminado")
                            await self.message.channel.send(embed=embed)
                            num_messages -= 1
                        else:
                            #Seleccionar mensaje aleatorio
                            normal_message = random.choice(normal_messages)

                            #Reemplazar {usuario1} y {usuario} con los nombres de usuario mencionados
                            normal_message = normal_message.replace("{usuario}", random.choice(participants).mention)
                            normal_message = normal_message.replace("{usuario1}", random.choice(participants).mention)
                            
                            # Generar un embed para el mensaje normal con la imagen
                            embed = Embed(title=f"**Dia {rounds}**", description=normal_message)
                            embed.set_image(url=normal_image_url)
                            
                            await self.message.channel.send(embed=embed)
                            num_messages -= 1

                    await asyncio.sleep(10)  # Esperar 10 segundos entre mensajes
                

            remaining_participants = ", ".join([member.mention for member in participants])
            await send_message(self.message.channel, f"¡Los participantes restantes son: {remaining_participants}!")
            await asyncio.sleep(20)  # Esperar 30 segundos entre rondas
            



        # Después de que queda solo un participante como ganador
        winner = participants[0]

        # Crear un embed para mencionar al ganador
        winner_embed = Embed(title="Ganador de los Hunger Games", description=f"¡El ganador es {winner.mention}!")
        winner_embed.set_image(url="https://i1.sndcdn.com/artworks-000091906989-vg6yx4-t500x500.jpg")

        # Enviar el embed al canal
        await self.message.channel.send(f"{winner.mention}:")
        await self.message.channel.send(embed=winner_embed)