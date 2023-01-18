from .types import CommandConfig, QueryConfig, EventConfig

from schedule.domain import events as schedule_events
from schedule import models as schedule_repos
from schedule.application import commands as schedule_commands
from schedule.application import handlers as schedule_handlers
from schedule import query_handlers as schedule_query_handlers
from schedule.application import queries as schedule_queries


Commands: CommandConfig = {
    schedule_commands.CreateSchedule: (
        schedule_handlers.CreateScheduleHandler,
        schedule_repos.ScheduleRepository,
    ),
    schedule_commands.PublishAppointedSchedules: (
        schedule_handlers.PublishAppointedHandler,
        schedule_repos.ScheduleRepository,
    ),

}


Queries: QueryConfig = {
    schedule_queries.ScheduleQuery: schedule_query_handlers.ScheduleQueryHandler,
}


Events: EventConfig = {
    schedule_events.CategoryAppointed: [  # these listeners are in another context which I didn't bring here
        (charge_listeners.CategoryAppointedListener, charge_repos.JobRepository)
    ],
}
