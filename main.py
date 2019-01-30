
# [START imports]
import endpoints
import agenda_enty
from endpoints import message_types
from endpoints import messages
from endpoints import remote
import logging

from google.appengine.ext import ndb
# [END imports]

# [START messages]
class AgendaRequest(messages.Message):
    nome = messages.StringField(1)
    telefone = messages.StringField(2)
    endereco = messages.StringField(3)
    agendaId = messages.StringField(4)

#class AgendaResponse(messages.Message):
 #   """A proto Message that contains a simple string field."""
 #   message = messages.MessageField(AgendaRequest, 1, repeated=True)
 #   #message = messages.StringField(1)
class AgendaResponse(messages.Message):
    """A proto Message that contains a simple string field."""    
    message = messages.StringField(1)
    agenda = messages.MessageField(AgendaRequest, 2, repeated=True)

AGENDA_RESOURCE = endpoints.ResourceContainer(
    AgendaRequest,
    n=messages.IntegerField(4, default=1))

class AgendaResponse2(messages.Message):
    """A proto Message that contains a simple string field."""    
    nome = messages.StringField(1)
    telefone = messages.StringField(2)
    endereco = messages.StringField(3)
    n = messages.IntegerField(4, default=1)


# [START agenda]
@endpoints.api(name='agenda', version='v1')
class Agenda(remote.Service):       
    @endpoints.method(
        # This method takes a ResourceContainer defined above.
        AGENDA_RESOURCE,
        # This method returns an Agenda message.
        AgendaResponse,
        path='agendas',
        http_method='POST',
        name='criar_agenda')
    def criar_agenda(self, request):
        #output_message = ' '.join([request.message] * request.n)        
        agenda= agenda_enty.Agenda()
        agenda.nome=request.nome
        agenda.telefone=request.telefone
        agenda.endereco=request.endereco        
        key=agenda.put()
        #output_message=agenda.nome+" "+agenda.telefone+" "+agenda.endereco        
        #return AgendaResponse(message=output_message)
        responseList=[]        
        responseList.append(AgendaRequest(nome=agenda.nome,telefone=agenda.telefone, endereco=agenda.endereco,agendaId=str(agenda.key.id()) ))
        return AgendaResponse(agenda=responseList)
        #return AgendaResponse(message=AgendaRequest(nome=agenda.nome,telefone=agenda.telefone, endereco=agenda.endereco,agendaId=str(agenda.key.id)))
    # [END salvarAgenda]
    
    @endpoints.method(
        # This method takes a ResourceContainer defined above.
        AGENDA_RESOURCE,
        # This method returns an Agenda message.
        AgendaResponse,
        path='agendas/{n}',
        http_method='DELETE',
        name='deletar_agenda')
    def deletar_agenda(self, request):
        retorno ="OK"
        agenda=agenda_enty.Agenda().get_agenda(request.n) 
        #retorno=agenda_enty.Agenda().delete_agenda(request.n)
        if(agenda!=None):
            agenda.key.delete()
            retorno= ":) Tudo OK"
        else:
            retorno= "Ops... Nao Cadastrado"
        
        agendaList=agenda_enty.Agenda.query()
        responseList=[]
        for agenda in agendaList:
            responseList.append(AgendaRequest(nome=agenda.nome,telefone=agenda.telefone, endereco=agenda.endereco,agendaId=str(agenda.key.id())))


        return AgendaResponse(message=retorno,agenda=responseList)


    @endpoints.method(
        # This method takes a ResourceContainer defined above.
        AGENDA_RESOURCE,
        # This method returns an Agenda message.
        AgendaResponse,
        path='agendas/{n}',
        http_method='PUT',
        name='atualizar_agenda')
    def atualizar_agenda(self, request):
       #teste=str(request.n)
        message_response=" "
        agenda=agenda_enty.Agenda().get_agenda(request.n)        
        responseList = []        
        if (agenda!=None):
            agenda.nome=request.nome if request.nome!= None else agenda.nome
            agenda.telefone=request.telefone if request.telefone!= None else agenda.telefone
            agenda.endereco=request.endereco if request.endereco!= None else agenda.endereco
            message_response="OK :)"               

        else:
            agenda= agenda_enty.Agenda()
            agenda.nome=request.nome
            agenda.telefone=request.telefone
            agenda.endereco=request.endereco           
            message_response="Criado novo Registro :)" 
            
        try:
            agenda.put()
            responseList.append(AgendaRequest(nome=agenda.nome,telefone=agenda.telefone, endereco=agenda.endereco,agendaId=str(agenda.key.id()) ))
        except:
            message_response="Not OK :(" 
            responseList.append(AgendaRequest())


        #return AgendaResponse(message=teste)
        return AgendaResponse(message=message_response,agenda=responseList)
    
    
    @endpoints.method(
        # This method takes a ResourceContainer defined above.
        AGENDA_RESOURCE,
        # This method returns an Agenda message.
        AgendaResponse,
        path='agendas',
        http_method='GET',
        name='agendas')
    def agendaList(self, request):             
               
        #agendaList=agenda_enty.Agenda.query().order(agenda_enty.Agenda.nome).fetch_page(5, start_cursor= 0 if request.n == None else request.n)
        #agendaList=agenda_enty.Agenda.query().order(agenda_enty.Agenda.nome).fetch_page(2,start_cursor=3)
        
        #agendaList=agenda_enty.Agenda.query().order(agenda_enty.Agenda.nome)
        
        agendaList=agenda_enty.Agenda.query(agenda_enty.Agenda.nome == request.nome).order(agenda_enty.Agenda.nome)
        
        responseList=[]
        for agenda in agendaList:
            responseList.append(AgendaRequest(nome=agenda.nome,telefone=agenda.telefone, endereco=agenda.endereco,agendaId=str(agenda.key.id())))
        #output_message=""
        #for agenda in agendaList:
         #   output_message+= agenda.nome+" "+agenda.telefone+" "+agenda.endereco+" "+str(agenda.key.id())
        #output_message=agenda.nome+" "+agenda.telefone+" "+agenda.endereco+" "+str(key)         
2019010712240016729
        return AgendaResponse(agenda=responseList)


    @endpoints.method(
        # This method takes a ResourceContainer defined above.
        AgendaResponse2,
        # This method returns an Agenda message.
        AgendaResponse,
        path='agendas/{nome}/{telefone}/{endereco}',
        http_method='GET',
        name='buscar_agenda')
    def buscar_agenda(self, request):
       #teste=str(request.n)
       
        logging.info("REQUEST {}".format(request))
        message_response=""
        logging.info("REQUEST {}".format(request.nome))

        agendaList=agenda_enty.Agenda.query(
                ndb.AND(agenda_enty.Agenda.nome == request.nome,
                        agenda_enty.Agenda.telefone == request.telefone,
                            agenda_enty.Agenda.endereco == request.endereco
                    )
        ).order(agenda_enty.Agenda.nome)
        
        logging.info("REQUEST {}".format(agendaList))
        
        responseList = []
        for agenda in agendaList:
              responseList.append(AgendaRequest(nome=agenda.nome,telefone=agenda.telefone, endereco=agenda.endereco,agendaId=str(agenda.key.id())))
    

        #agenda=agenda_enty.Agenda().get_agenda(request.n)        
       
        #responseList = []        
        #if(agenda!=None):
        #    message_response="OK :)"
        #    responseList.append(AgendaRequest(nome=agenda.nome,telefone=agenda.telefone, endereco=agenda.endereco,agendaId=str(agenda.key.id()) ))              
        #else:                      
            
        #    agendaList=agenda_enty.Agenda.query().order(agenda_enty.Agenda.nome)
        #    for agenda in agendaList:
        #        responseList.append(AgendaRequest(nome=agenda.nome,telefone=agenda.telefone, endereco=agenda.endereco,agendaId=str(agenda.key.id())))
        #    message_response="Not OK :("
        
        #return AgendaResponse(message=teste)
        return AgendaResponse(message=message_response,agenda=responseList)   
    # [END ListaAgenda]
    def factoryResponse(self,agendaList):
            responseList=[]
            for agenda in agendaList:
                responseList.append(AgendaRequest(nome=agenda.nome,teleFone=agenda.telefone, endereco=agenda.endereco,agendaId=agenda.key.id()))
            return responseList
    
# [END agenda]

#[Inico  Teste]
class TesteResponse(messages.Message):
    """A proto Message that contains a simple string field."""    
    message = messages.StringField(1)


# [END messages]
@endpoints.api(name='teste', version='v1')
class Teste(remote.Service):
    @endpoints.method(
        # This method takes a ResourceContainer defined above.
        message_types.VoidMessage,
        # This method returns an Echo message.
        TesteResponse,
        path='teste',
        http_method='GET',
        name='teste')
    def index(self, request):
        #output_message = ' '.join([request.message] * request.n)  
        user = endpoints.get_current_user()
        user_name = user.email() if user else 'Anonymous'             
        return TesteResponse(message='Hello, {}'.format(user_name)) 
        # [END index]


# [START api_server]
api = endpoints.api_server([Agenda,Teste])
# [END api_server]]
