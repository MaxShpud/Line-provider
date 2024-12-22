from uuid import UUID

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends

from app.api.rest.errors import ACTIVE_EVENT_ALREADY_EXISTS_HTTP_ERROR, RETRIEVE_EVENT_HTTP_ERROR, \
    UPDATE_EVENT_HTTP_ERROR
from app.api.rest.public.v1.view_models import EventViewModel, CreateEventViewModel, UpdateEventViewModel, \
    EventListViewModel
from app.app_layer.use_cases.event.create_event import CreateEventUseCase
from app.app_layer.use_cases.event.dto import EventRetrieveInputDTO
from app.app_layer.use_cases.event.event_list import EventListUseCase
from app.app_layer.use_cases.event.retrieve_event import RetrieveEventUseCase
from app.app_layer.use_cases.event.update_event import UpdateEventUseCase
from app.containers import Container
from app.domain.interfaces.repositories.event.exceptions import ActiveEventAlreadyExistsError, EventNotFoundError, \
    EventUpdateError

router = APIRouter()


@router.post("")
@inject
async def create(
        data: CreateEventViewModel,
        use_case: CreateEventUseCase = Depends(Provide[Container.create_event_use_case])
) -> EventViewModel:
    try:
        result = await use_case.create_event(coefficient=data.coefficient,
                                            deadline=data.deadline,
                                            status=data.status,
                                            event_type=data.type,
                                            info=data.info,)
    except ActiveEventAlreadyExistsError:
        raise ACTIVE_EVENT_ALREADY_EXISTS_HTTP_ERROR

    return EventViewModel.model_validate(result)


@router.get('/{event_id}')
@inject
async def retrieve(
        event_id: UUID,
        use_case: RetrieveEventUseCase = Depends(Provide[Container.retrieve_event_use_case])
) -> EventViewModel:
    try:
        result = await use_case.execute(
            data=EventRetrieveInputDTO(
                event_id=event_id,
            )
        )
    except EventNotFoundError:
        raise RETRIEVE_EVENT_HTTP_ERROR
    return EventViewModel.model_validate(result)

@router.put('')
@inject
async def update(
        data: UpdateEventViewModel,
        use_case: UpdateEventUseCase = Depends(Provide[Container.update_event_use_case]),
) -> EventViewModel:
    try:
        result = await use_case.execute(
            event_id=data.id,
            coefficient=data.coefficient,
            deadline=data.deadline,
            status=data.status,
            event_type=data.type,
            info=data.info,
        )
    except EventUpdateError:
        raise UPDATE_EVENT_HTTP_ERROR
    return EventViewModel.model_validate(result)

@router.get('s')
@inject
async def get_list(
        use_case: EventListUseCase = Depends(Provide[Container.event_list_use_case])
) -> EventListViewModel:
    try:
        result = await use_case.execute()
        validated_events = [EventViewModel.model_validate(event) for event in result]
    except EventNotFoundError:
        raise RETRIEVE_EVENT_HTTP_ERROR
    return EventListViewModel(events=validated_events)