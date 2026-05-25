from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.features.auth.model import User
from app.features.tickets.model import Ticket
from app.features.tickets.schema import TicketCreate, TicketStatusUpdate


def create_ticket(db: Session, data: TicketCreate, current_user: User) -> Ticket:
    ticket = Ticket(
        title=data.title,
        description=data.description,
        priority=data.priority,
        owner_id=current_user.id,
    )
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    return ticket


def list_tickets(db: Session, current_user: User) -> list[Ticket]:
    return db.query(Ticket).filter(Ticket.owner_id == current_user.id).order_by(Ticket.id.desc()).all()


def update_ticket_status(
    db: Session,
    ticket_id: int,
    data: TicketStatusUpdate,
    current_user: User,
) -> Ticket:
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id, Ticket.owner_id == current_user.id).first()
    if ticket is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found",
        )

    ticket.status = data.status
    db.commit()
    db.refresh(ticket)
    return ticket


def delete_ticket(db: Session, ticket_id: int, current_user: User) -> None:
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id, Ticket.owner_id == current_user.id).first()
    if ticket is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found",
        )

    db.delete(ticket)
    db.commit()
