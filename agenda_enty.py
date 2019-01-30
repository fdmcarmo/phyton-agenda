from google.appengine.ext import ndb

class Agenda(ndb.Model): 
    
    nome = ndb.StringProperty()
    telefone = ndb.StringProperty()
    endereco = ndb.StringProperty()
   
    def get_agenda(self,chave):
        #return Agenda.query(Agenda.key == ndb.Key(Agenda, teste)).get(keys_only=True)
        return ndb.Key('Agenda', chave).get()
    
    def delete_agenda(self,chave):
        #return Agenda.query(Agenda.key == ndb.Key(Agenda, teste)).get(keys_only=True)
        try:
            chave.key.delete()
            return "ok"
        except:    
            return "Ops... No OK"