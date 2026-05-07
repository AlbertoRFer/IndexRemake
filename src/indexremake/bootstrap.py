from indexremake import app, services
from indexremake.bridge import presenters
from indexremake.infrastructure.persistence import database


def create_index_app(db: database.SQLiteDatabase) -> app.IndexApp:
    doc_service = services.DocumentService(db)
    main_presenter = presenters.MainPresenter(doc_service)
    presenters.MainPresenter.set_instance(main_presenter)

    return app.IndexApp()
