from flask import Blueprint, render_template

error_handlers_bp = Blueprint('error_handlers', __name__)

@error_handlers_bp.app_errorhandler(404)
def page_not_found(e):
    return render_template("error.html", error=f"{e.code} {e.description}", code=f"img/{e.code}.png"), 404

@error_handlers_bp.app_errorhandler(403)
def page_not_found(e):
    return render_template("error.html", error=f"{e.code} {e.description}", code=f"img/{e.code}.png"), 403

@error_handlers_bp.app_errorhandler(451)
def legal_reasons(e):
    return render_template("error.html", error=f"{e.code} {e.description}", code=f"img/{e.code}.png"), 451

@error_handlers_bp.app_errorhandler(500)
def server_error(e):
    return render_template("error.html", error=f"{e.code} {e.description}", code=f"img/{e.code}.png"), 500