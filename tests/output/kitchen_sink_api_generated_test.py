
import logging
from dataclasses import dataclass
from linkml_dataops.query.queryengine import QueryEngine
from linkml_dataops.query.query_model import FetchQuery, Constraint, MatchConstraint, OrConstraint, AbstractQuery,     FetchById
from linkml_dataops.query.queryengine import MatchExpression

from tests.model.kitchen_sink import *

@dataclass
class KitchenSinkAPI:

    # attributes
    query_engine: QueryEngine = None

    
    # --
    # Any methods
    # --
    def fetch_Any(self, id_value: str) -> Any:
        """
        Retrieves an instance of `Any` via a primary key

        :param id_value:
        :return: Any with matching ID
        """
        q = FetchById(id=id_value, target_class=Any.class_name)
        results = self.query_engine.fetch_by_id(q)
        return results[0] if results else None

    def query_Any(self,
             
             _extra: Any = None) -> List[Any]:
        """
        Queries for instances of `Any`

        
        :return: Person list matching constraints
        """
        results = self.query_engine.simple_query(Any.class_name,
                                                 
                                                 _extra=_extra)
        return results
    
    # --
    # HasAliases methods
    # --
    def fetch_HasAliases(self, id_value: str) -> HasAliases:
        """
        Retrieves an instance of `HasAliases` via a primary key

        :param id_value:
        :return: HasAliases with matching ID
        """
        q = FetchById(id=id_value, target_class=HasAliases.class_name)
        results = self.query_engine.fetch_by_id(q)
        return results[0] if results else None

    def query_HasAliases(self,
             aliases: Union[str, MatchExpression] = None,
             
             _extra: Any = None) -> List[HasAliases]:
        """
        Queries for instances of `HasAliases`

        :param aliases: None
        
        :return: Person list matching constraints
        """
        results = self.query_engine.simple_query(HasAliases.class_name,
                                                 
                                                 aliases=aliases,
                                                 
                                                 _extra=_extra)
        return results
    
    # --
    # Thing methods
    # --
    def fetch_Thing(self, id_value: str) -> Thing:
        """
        Retrieves an instance of `Thing` via a primary key

        :param id_value:
        :return: Thing with matching ID
        """
        q = FetchById(id=id_value, target_class=Thing.class_name)
        results = self.query_engine.fetch_by_id(q)
        return results[0] if results else None

    def query_Thing(self,
             id: Union[str, MatchExpression] = None,
             name: Union[str, MatchExpression] = None,
             
             _extra: Any = None) -> List[Thing]:
        """
        Queries for instances of `Thing`

        :param id: None
        :param name: None
        
        :return: Person list matching constraints
        """
        results = self.query_engine.simple_query(Thing.class_name,
                                                 
                                                 id=id,
                                                 
                                                 name=name,
                                                 
                                                 _extra=_extra)
        return results
    
    # --
    # Person methods
    # --
    def fetch_Person(self, id_value: str) -> Person:
        """
        Retrieves an instance of `Person` via a primary key

        :param id_value:
        :return: Person with matching ID
        """
        q = FetchById(id=id_value, target_class=Person.class_name)
        results = self.query_engine.fetch_by_id(q)
        return results[0] if results else None

    def query_Person(self,
             has_employment_history: Union[str, MatchExpression] = None,
             has_familial_relationships: Union[str, MatchExpression] = None,
             has_medical_history: Union[str, MatchExpression] = None,
             age_in_years: Union[str, MatchExpression] = None,
             addresses: Union[str, MatchExpression] = None,
             has_birth_event: Union[str, MatchExpression] = None,
             metadata: Union[str, MatchExpression] = None,
             aliases: Union[str, MatchExpression] = None,
             id: Union[str, MatchExpression] = None,
             name: Union[str, MatchExpression] = None,
             
             _extra: Any = None) -> List[Person]:
        """
        Queries for instances of `Person`

        :param has_employment_history: None
        :param has_familial_relationships: None
        :param has_medical_history: None
        :param age_in_years: None
        :param addresses: None
        :param has_birth_event: None
        :param metadata: None
        :param aliases: None
        :param id: None
        :param name: None
        
        :return: Person list matching constraints
        """
        results = self.query_engine.simple_query(Person.class_name,
                                                 
                                                 has_employment_history=has_employment_history,
                                                 
                                                 has_familial_relationships=has_familial_relationships,
                                                 
                                                 has_medical_history=has_medical_history,
                                                 
                                                 age_in_years=age_in_years,
                                                 
                                                 addresses=addresses,
                                                 
                                                 has_birth_event=has_birth_event,
                                                 
                                                 metadata=metadata,
                                                 
                                                 aliases=aliases,
                                                 
                                                 id=id,
                                                 
                                                 name=name,
                                                 
                                                 _extra=_extra)
        return results
    
    # --
    # Adult methods
    # --
    def fetch_Adult(self, id_value: str) -> Adult:
        """
        Retrieves an instance of `Adult` via a primary key

        :param id_value:
        :return: Adult with matching ID
        """
        q = FetchById(id=id_value, target_class=Adult.class_name)
        results = self.query_engine.fetch_by_id(q)
        return results[0] if results else None

    def query_Adult(self,
             has_employment_history: Union[str, MatchExpression] = None,
             has_familial_relationships: Union[str, MatchExpression] = None,
             has_medical_history: Union[str, MatchExpression] = None,
             age_in_years: Union[str, MatchExpression] = None,
             addresses: Union[str, MatchExpression] = None,
             has_birth_event: Union[str, MatchExpression] = None,
             metadata: Union[str, MatchExpression] = None,
             aliases: Union[str, MatchExpression] = None,
             id: Union[str, MatchExpression] = None,
             name: Union[str, MatchExpression] = None,
             
             _extra: Any = None) -> List[Adult]:
        """
        Queries for instances of `Adult`

        :param has_employment_history: None
        :param has_familial_relationships: None
        :param has_medical_history: None
        :param age_in_years: None
        :param addresses: None
        :param has_birth_event: None
        :param metadata: None
        :param aliases: None
        :param id: None
        :param name: None
        
        :return: Person list matching constraints
        """
        results = self.query_engine.simple_query(Adult.class_name,
                                                 
                                                 has_employment_history=has_employment_history,
                                                 
                                                 has_familial_relationships=has_familial_relationships,
                                                 
                                                 has_medical_history=has_medical_history,
                                                 
                                                 age_in_years=age_in_years,
                                                 
                                                 addresses=addresses,
                                                 
                                                 has_birth_event=has_birth_event,
                                                 
                                                 metadata=metadata,
                                                 
                                                 aliases=aliases,
                                                 
                                                 id=id,
                                                 
                                                 name=name,
                                                 
                                                 _extra=_extra)
        return results
    
    # --
    # Organization methods
    # --
    def fetch_Organization(self, id_value: str) -> Organization:
        """
        Retrieves an instance of `Organization` via a primary key

        :param id_value:
        :return: Organization with matching ID
        """
        q = FetchById(id=id_value, target_class=Organization.class_name)
        results = self.query_engine.fetch_by_id(q)
        return results[0] if results else None

    def query_Organization(self,
             aliases: Union[str, MatchExpression] = None,
             id: Union[str, MatchExpression] = None,
             name: Union[str, MatchExpression] = None,
             
             _extra: Any = None) -> List[Organization]:
        """
        Queries for instances of `Organization`

        :param aliases: None
        :param id: None
        :param name: None
        
        :return: Person list matching constraints
        """
        results = self.query_engine.simple_query(Organization.class_name,
                                                 
                                                 aliases=aliases,
                                                 
                                                 id=id,
                                                 
                                                 name=name,
                                                 
                                                 _extra=_extra)
        return results
    
    # --
    # Place methods
    # --
    def fetch_Place(self, id_value: str) -> Place:
        """
        Retrieves an instance of `Place` via a primary key

        :param id_value:
        :return: Place with matching ID
        """
        q = FetchById(id=id_value, target_class=Place.class_name)
        results = self.query_engine.fetch_by_id(q)
        return results[0] if results else None

    def query_Place(self,
             id: Union[str, MatchExpression] = None,
             name: Union[str, MatchExpression] = None,
             aliases: Union[str, MatchExpression] = None,
             
             _extra: Any = None) -> List[Place]:
        """
        Queries for instances of `Place`

        :param id: None
        :param name: None
        :param aliases: None
        
        :return: Person list matching constraints
        """
        results = self.query_engine.simple_query(Place.class_name,
                                                 
                                                 id=id,
                                                 
                                                 name=name,
                                                 
                                                 aliases=aliases,
                                                 
                                                 _extra=_extra)
        return results
    
    # --
    # Address methods
    # --
    def fetch_Address(self, id_value: str) -> Address:
        """
        Retrieves an instance of `Address` via a primary key

        :param id_value:
        :return: Address with matching ID
        """
        q = FetchById(id=id_value, target_class=Address.class_name)
        results = self.query_engine.fetch_by_id(q)
        return results[0] if results else None

    def query_Address(self,
             street: Union[str, MatchExpression] = None,
             city: Union[str, MatchExpression] = None,
             
             _extra: Any = None) -> List[Address]:
        """
        Queries for instances of `Address`

        :param street: None
        :param city: None
        
        :return: Person list matching constraints
        """
        results = self.query_engine.simple_query(Address.class_name,
                                                 
                                                 street=street,
                                                 
                                                 city=city,
                                                 
                                                 _extra=_extra)
        return results
    
    # --
    # Concept methods
    # --
    def fetch_Concept(self, id_value: str) -> Concept:
        """
        Retrieves an instance of `Concept` via a primary key

        :param id_value:
        :return: Concept with matching ID
        """
        q = FetchById(id=id_value, target_class=Concept.class_name)
        results = self.query_engine.fetch_by_id(q)
        return results[0] if results else None

    def query_Concept(self,
             id: Union[str, MatchExpression] = None,
             name: Union[str, MatchExpression] = None,
             
             _extra: Any = None) -> List[Concept]:
        """
        Queries for instances of `Concept`

        :param id: None
        :param name: None
        
        :return: Person list matching constraints
        """
        results = self.query_engine.simple_query(Concept.class_name,
                                                 
                                                 id=id,
                                                 
                                                 name=name,
                                                 
                                                 _extra=_extra)
        return results
    
    # --
    # DiagnosisConcept methods
    # --
    def fetch_DiagnosisConcept(self, id_value: str) -> DiagnosisConcept:
        """
        Retrieves an instance of `DiagnosisConcept` via a primary key

        :param id_value:
        :return: DiagnosisConcept with matching ID
        """
        q = FetchById(id=id_value, target_class=DiagnosisConcept.class_name)
        results = self.query_engine.fetch_by_id(q)
        return results[0] if results else None

    def query_DiagnosisConcept(self,
             id: Union[str, MatchExpression] = None,
             name: Union[str, MatchExpression] = None,
             
             _extra: Any = None) -> List[DiagnosisConcept]:
        """
        Queries for instances of `DiagnosisConcept`

        :param id: None
        :param name: None
        
        :return: Person list matching constraints
        """
        results = self.query_engine.simple_query(DiagnosisConcept.class_name,
                                                 
                                                 id=id,
                                                 
                                                 name=name,
                                                 
                                                 _extra=_extra)
        return results
    
    # --
    # ProcedureConcept methods
    # --
    def fetch_ProcedureConcept(self, id_value: str) -> ProcedureConcept:
        """
        Retrieves an instance of `ProcedureConcept` via a primary key

        :param id_value:
        :return: ProcedureConcept with matching ID
        """
        q = FetchById(id=id_value, target_class=ProcedureConcept.class_name)
        results = self.query_engine.fetch_by_id(q)
        return results[0] if results else None

    def query_ProcedureConcept(self,
             id: Union[str, MatchExpression] = None,
             name: Union[str, MatchExpression] = None,
             
             _extra: Any = None) -> List[ProcedureConcept]:
        """
        Queries for instances of `ProcedureConcept`

        :param id: None
        :param name: None
        
        :return: Person list matching constraints
        """
        results = self.query_engine.simple_query(ProcedureConcept.class_name,
                                                 
                                                 id=id,
                                                 
                                                 name=name,
                                                 
                                                 _extra=_extra)
        return results
    
    # --
    # Event methods
    # --
    def fetch_Event(self, id_value: str) -> Event:
        """
        Retrieves an instance of `Event` via a primary key

        :param id_value:
        :return: Event with matching ID
        """
        q = FetchById(id=id_value, target_class=Event.class_name)
        results = self.query_engine.fetch_by_id(q)
        return results[0] if results else None

    def query_Event(self,
             started_at_time: Union[str, MatchExpression] = None,
             ended_at_time: Union[str, MatchExpression] = None,
             is_current: Union[str, MatchExpression] = None,
             
             _extra: Any = None) -> List[Event]:
        """
        Queries for instances of `Event`

        :param started_at_time: None
        :param ended_at_time: None
        :param is_current: None
        
        :return: Person list matching constraints
        """
        results = self.query_engine.simple_query(Event.class_name,
                                                 
                                                 started_at_time=started_at_time,
                                                 
                                                 ended_at_time=ended_at_time,
                                                 
                                                 is_current=is_current,
                                                 
                                                 _extra=_extra)
        return results
    
    # --
    # Relationship methods
    # --
    def fetch_Relationship(self, id_value: str) -> Relationship:
        """
        Retrieves an instance of `Relationship` via a primary key

        :param id_value:
        :return: Relationship with matching ID
        """
        q = FetchById(id=id_value, target_class=Relationship.class_name)
        results = self.query_engine.fetch_by_id(q)
        return results[0] if results else None

    def query_Relationship(self,
             started_at_time: Union[str, MatchExpression] = None,
             ended_at_time: Union[str, MatchExpression] = None,
             related_to: Union[str, MatchExpression] = None,
             type: Union[str, MatchExpression] = None,
             
             _extra: Any = None) -> List[Relationship]:
        """
        Queries for instances of `Relationship`

        :param started_at_time: None
        :param ended_at_time: None
        :param related_to: None
        :param type: None
        
        :return: Person list matching constraints
        """
        results = self.query_engine.simple_query(Relationship.class_name,
                                                 
                                                 started_at_time=started_at_time,
                                                 
                                                 ended_at_time=ended_at_time,
                                                 
                                                 related_to=related_to,
                                                 
                                                 type=type,
                                                 
                                                 _extra=_extra)
        return results
    
    # --
    # FamilialRelationship methods
    # --
    def fetch_FamilialRelationship(self, id_value: str) -> FamilialRelationship:
        """
        Retrieves an instance of `FamilialRelationship` via a primary key

        :param id_value:
        :return: FamilialRelationship with matching ID
        """
        q = FetchById(id=id_value, target_class=FamilialRelationship.class_name)
        results = self.query_engine.fetch_by_id(q)
        return results[0] if results else None

    def query_FamilialRelationship(self,
             started_at_time: Union[str, MatchExpression] = None,
             ended_at_time: Union[str, MatchExpression] = None,
             related_to: Union[str, MatchExpression] = None,
             type: Union[str, MatchExpression] = None,
             
             _extra: Any = None) -> List[FamilialRelationship]:
        """
        Queries for instances of `FamilialRelationship`

        :param started_at_time: None
        :param ended_at_time: None
        :param related_to: None
        :param type: None
        
        :return: Person list matching constraints
        """
        results = self.query_engine.simple_query(FamilialRelationship.class_name,
                                                 
                                                 started_at_time=started_at_time,
                                                 
                                                 ended_at_time=ended_at_time,
                                                 
                                                 related_to=related_to,
                                                 
                                                 type=type,
                                                 
                                                 _extra=_extra)
        return results
    
    # --
    # BirthEvent methods
    # --
    def fetch_BirthEvent(self, id_value: str) -> BirthEvent:
        """
        Retrieves an instance of `BirthEvent` via a primary key

        :param id_value:
        :return: BirthEvent with matching ID
        """
        q = FetchById(id=id_value, target_class=BirthEvent.class_name)
        results = self.query_engine.fetch_by_id(q)
        return results[0] if results else None

    def query_BirthEvent(self,
             in_location: Union[str, MatchExpression] = None,
             started_at_time: Union[str, MatchExpression] = None,
             ended_at_time: Union[str, MatchExpression] = None,
             is_current: Union[str, MatchExpression] = None,
             
             _extra: Any = None) -> List[BirthEvent]:
        """
        Queries for instances of `BirthEvent`

        :param in_location: None
        :param started_at_time: None
        :param ended_at_time: None
        :param is_current: None
        
        :return: Person list matching constraints
        """
        results = self.query_engine.simple_query(BirthEvent.class_name,
                                                 
                                                 in_location=in_location,
                                                 
                                                 started_at_time=started_at_time,
                                                 
                                                 ended_at_time=ended_at_time,
                                                 
                                                 is_current=is_current,
                                                 
                                                 _extra=_extra)
        return results
    
    # --
    # EmploymentEvent methods
    # --
    def fetch_EmploymentEvent(self, id_value: str) -> EmploymentEvent:
        """
        Retrieves an instance of `EmploymentEvent` via a primary key

        :param id_value:
        :return: EmploymentEvent with matching ID
        """
        q = FetchById(id=id_value, target_class=EmploymentEvent.class_name)
        results = self.query_engine.fetch_by_id(q)
        return results[0] if results else None

    def query_EmploymentEvent(self,
             employed_at: Union[str, MatchExpression] = None,
             started_at_time: Union[str, MatchExpression] = None,
             ended_at_time: Union[str, MatchExpression] = None,
             is_current: Union[str, MatchExpression] = None,
             
             _extra: Any = None) -> List[EmploymentEvent]:
        """
        Queries for instances of `EmploymentEvent`

        :param employed_at: None
        :param started_at_time: None
        :param ended_at_time: None
        :param is_current: None
        
        :return: Person list matching constraints
        """
        results = self.query_engine.simple_query(EmploymentEvent.class_name,
                                                 
                                                 employed_at=employed_at,
                                                 
                                                 started_at_time=started_at_time,
                                                 
                                                 ended_at_time=ended_at_time,
                                                 
                                                 is_current=is_current,
                                                 
                                                 _extra=_extra)
        return results
    
    # --
    # MedicalEvent methods
    # --
    def fetch_MedicalEvent(self, id_value: str) -> MedicalEvent:
        """
        Retrieves an instance of `MedicalEvent` via a primary key

        :param id_value:
        :return: MedicalEvent with matching ID
        """
        q = FetchById(id=id_value, target_class=MedicalEvent.class_name)
        results = self.query_engine.fetch_by_id(q)
        return results[0] if results else None

    def query_MedicalEvent(self,
             in_location: Union[str, MatchExpression] = None,
             diagnosis: Union[str, MatchExpression] = None,
             procedure: Union[str, MatchExpression] = None,
             started_at_time: Union[str, MatchExpression] = None,
             ended_at_time: Union[str, MatchExpression] = None,
             is_current: Union[str, MatchExpression] = None,
             
             _extra: Any = None) -> List[MedicalEvent]:
        """
        Queries for instances of `MedicalEvent`

        :param in_location: None
        :param diagnosis: None
        :param procedure: None
        :param started_at_time: None
        :param ended_at_time: None
        :param is_current: None
        
        :return: Person list matching constraints
        """
        results = self.query_engine.simple_query(MedicalEvent.class_name,
                                                 
                                                 in_location=in_location,
                                                 
                                                 diagnosis=diagnosis,
                                                 
                                                 procedure=procedure,
                                                 
                                                 started_at_time=started_at_time,
                                                 
                                                 ended_at_time=ended_at_time,
                                                 
                                                 is_current=is_current,
                                                 
                                                 _extra=_extra)
        return results
    
    # --
    # WithLocation methods
    # --
    def fetch_WithLocation(self, id_value: str) -> WithLocation:
        """
        Retrieves an instance of `WithLocation` via a primary key

        :param id_value:
        :return: WithLocation with matching ID
        """
        q = FetchById(id=id_value, target_class=WithLocation.class_name)
        results = self.query_engine.fetch_by_id(q)
        return results[0] if results else None

    def query_WithLocation(self,
             in_location: Union[str, MatchExpression] = None,
             
             _extra: Any = None) -> List[WithLocation]:
        """
        Queries for instances of `WithLocation`

        :param in_location: None
        
        :return: Person list matching constraints
        """
        results = self.query_engine.simple_query(WithLocation.class_name,
                                                 
                                                 in_location=in_location,
                                                 
                                                 _extra=_extra)
        return results
    
    # --
    # MarriageEvent methods
    # --
    def fetch_MarriageEvent(self, id_value: str) -> MarriageEvent:
        """
        Retrieves an instance of `MarriageEvent` via a primary key

        :param id_value:
        :return: MarriageEvent with matching ID
        """
        q = FetchById(id=id_value, target_class=MarriageEvent.class_name)
        results = self.query_engine.fetch_by_id(q)
        return results[0] if results else None

    def query_MarriageEvent(self,
             married_to: Union[str, MatchExpression] = None,
             in_location: Union[str, MatchExpression] = None,
             started_at_time: Union[str, MatchExpression] = None,
             ended_at_time: Union[str, MatchExpression] = None,
             is_current: Union[str, MatchExpression] = None,
             
             _extra: Any = None) -> List[MarriageEvent]:
        """
        Queries for instances of `MarriageEvent`

        :param married_to: None
        :param in_location: None
        :param started_at_time: None
        :param ended_at_time: None
        :param is_current: None
        
        :return: Person list matching constraints
        """
        results = self.query_engine.simple_query(MarriageEvent.class_name,
                                                 
                                                 married_to=married_to,
                                                 
                                                 in_location=in_location,
                                                 
                                                 started_at_time=started_at_time,
                                                 
                                                 ended_at_time=ended_at_time,
                                                 
                                                 is_current=is_current,
                                                 
                                                 _extra=_extra)
        return results
    
    # --
    # Company methods
    # --
    def fetch_Company(self, id_value: str) -> Company:
        """
        Retrieves an instance of `Company` via a primary key

        :param id_value:
        :return: Company with matching ID
        """
        q = FetchById(id=id_value, target_class=Company.class_name)
        results = self.query_engine.fetch_by_id(q)
        return results[0] if results else None

    def query_Company(self,
             ceo: Union[str, MatchExpression] = None,
             aliases: Union[str, MatchExpression] = None,
             id: Union[str, MatchExpression] = None,
             name: Union[str, MatchExpression] = None,
             
             _extra: Any = None) -> List[Company]:
        """
        Queries for instances of `Company`

        :param ceo: None
        :param aliases: None
        :param id: None
        :param name: None
        
        :return: Person list matching constraints
        """
        results = self.query_engine.simple_query(Company.class_name,
                                                 
                                                 ceo=ceo,
                                                 
                                                 aliases=aliases,
                                                 
                                                 id=id,
                                                 
                                                 name=name,
                                                 
                                                 _extra=_extra)
        return results
    
    # --
    # Dataset methods
    # --
    def fetch_Dataset(self, id_value: str) -> Dataset:
        """
        Retrieves an instance of `Dataset` via a primary key

        :param id_value:
        :return: Dataset with matching ID
        """
        q = FetchById(id=id_value, target_class=Dataset.class_name)
        results = self.query_engine.fetch_by_id(q)
        return results[0] if results else None

    def query_Dataset(self,
             persons: Union[str, MatchExpression] = None,
             companies: Union[str, MatchExpression] = None,
             activities: Union[str, MatchExpression] = None,
             
             _extra: Any = None) -> List[Dataset]:
        """
        Queries for instances of `Dataset`

        :param persons: None
        :param companies: None
        :param activities: None
        
        :return: Person list matching constraints
        """
        results = self.query_engine.simple_query(Dataset.class_name,
                                                 
                                                 persons=persons,
                                                 
                                                 companies=companies,
                                                 
                                                 activities=activities,
                                                 
                                                 _extra=_extra)
        return results
    
    # --
    # Activity methods
    # --
    def fetch_Activity(self, id_value: str) -> Activity:
        """
        Retrieves an instance of `Activity` via a primary key

        :param id_value:
        :return: Activity with matching ID
        """
        q = FetchById(id=id_value, target_class=Activity.class_name)
        results = self.query_engine.fetch_by_id(q)
        return results[0] if results else None

    def query_Activity(self,
             id: Union[str, MatchExpression] = None,
             started_at_time: Union[str, MatchExpression] = None,
             ended_at_time: Union[str, MatchExpression] = None,
             was_informed_by: Union[str, MatchExpression] = None,
             was_associated_with: Union[str, MatchExpression] = None,
             used: Union[str, MatchExpression] = None,
             description: Union[str, MatchExpression] = None,
             
             _extra: Any = None) -> List[Activity]:
        """
        Queries for instances of `Activity`

        :param id: None
        :param started_at_time: None
        :param ended_at_time: None
        :param was_informed_by: None
        :param was_associated_with: None
        :param used: None
        :param description: None
        
        :return: Person list matching constraints
        """
        results = self.query_engine.simple_query(Activity.class_name,
                                                 
                                                 id=id,
                                                 
                                                 started_at_time=started_at_time,
                                                 
                                                 ended_at_time=ended_at_time,
                                                 
                                                 was_informed_by=was_informed_by,
                                                 
                                                 was_associated_with=was_associated_with,
                                                 
                                                 used=used,
                                                 
                                                 description=description,
                                                 
                                                 _extra=_extra)
        return results
    
    # --
    # Agent methods
    # --
    def fetch_Agent(self, id_value: str) -> Agent:
        """
        Retrieves an instance of `Agent` via a primary key

        :param id_value:
        :return: Agent with matching ID
        """
        q = FetchById(id=id_value, target_class=Agent.class_name)
        results = self.query_engine.fetch_by_id(q)
        return results[0] if results else None

    def query_Agent(self,
             id: Union[str, MatchExpression] = None,
             acted_on_behalf_of: Union[str, MatchExpression] = None,
             was_informed_by: Union[str, MatchExpression] = None,
             
             _extra: Any = None) -> List[Agent]:
        """
        Queries for instances of `Agent`

        :param id: None
        :param acted_on_behalf_of: None
        :param was_informed_by: None
        
        :return: Person list matching constraints
        """
        results = self.query_engine.simple_query(Agent.class_name,
                                                 
                                                 id=id,
                                                 
                                                 acted_on_behalf_of=acted_on_behalf_of,
                                                 
                                                 was_informed_by=was_informed_by,
                                                 
                                                 _extra=_extra)
        return results
    
