from shared.application.interfaces import Listener
from discovery.domain.events import IndexCommitted  # this event is implemented in another context
from schedule.models import ScheduleRepository


class IndexCommittedListener(Listener):
    def handle(self, event: IndexCommitted, repo: ScheduleRepository) -> str:
        pass
