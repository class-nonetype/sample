from logging import Formatter

LOG_MESSAGE_FORMAT = '%(asctime)-10s %(levelname)-10s %(filename)-10s -> %(funcName)s::%(lineno)s: %(message)s'
LOG_DATE_FORMAT = '%d/%m/%Y %I:%M:%S %p'

LOG_FORMATTER = Formatter(fmt=LOG_MESSAGE_FORMAT, datefmt=LOG_DATE_FORMAT, style='%')


FILE_SIZE_FORMAT = '{:.2f} MB'

'''
def build_ticket_email_body(code: str, request_type: str | None, note: str | None = None) -> str:
    """
    Plantilla HTML con estilo minimalista (inspiración Angular Material) para notificar creación/actualización de tickets.
    """
    request_text = request_type or 'Ticket'
    sanitized_note = (note or '').strip()

    return f"""
    <!doctype html>
    <html>
    <head>
      <meta charset="utf-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <meta name="color-scheme" content="light">
      <meta name="supported-color-schemes" content="light">
      <style>
        :root {{ color-scheme: light; }}
        body, .email-bg {{ background:#f8fafc !important; color:#111827 !important; }}
        .card {{ background:#ffffff !important; border-radius:12px; border:1px solid #e5e7eb; overflow:hidden; }}
        .badge {{ background:#e6efff; color:#0f1b40; }}
        .muted {{ color:#6b7280; }}
        .cta {{ background:#1565c0; color:#ffffff; }}
        @media (prefers-color-scheme: dark) {{
          /* Evita que clientes de Windows inviertan los colores y dejen el texto ilegible. */
          :root {{ color-scheme: light; }}
        }}
        @media only screen and (max-width: 520px) {{
          body.email-bg {{ padding:12px !important; }}
          .card {{ max-width:480px !important; border-radius:10px !important; }}
          .content {{ padding:14px 12px 16px !important; }}
          .title {{ font-size:20px !important; }}
          .subtitle {{ font-size:13px !important; }}
          .cta {{ width:100% !important; min-width:0 !important; display:block !important; }}
        }}
      </style>
    </head>
    <body bgcolor="#f8fafc" class="email-bg" style="margin:0;padding:16px;background:#f8fafc;font-family:Roboto,'Segoe UI',Arial,sans-serif;color:#111827;">
      <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" bgcolor="#f8fafc" style="border-collapse:collapse;margin:0 auto;padding:0;background:#f8fafc;">
        <tr>
          <td align="center" style="padding:0;">
            <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" bgcolor="#ffffff" class="card" style="max-width:640px;width:100%;background:#ffffff;border-radius:12px;border:1px solid #e5e7eb;overflow:hidden;">
              <tr>
                <td style="height:6px;background:linear-gradient(90deg,#1e88e5,#1565c0);padding:0;margin:0;font-size:0;line-height:0;">&nbsp;</td>
              </tr>
              <tr>
                <td bgcolor="#ffffff" class="content" style="padding:18px 16px 20px;background:#ffffff;">
                  <span class="badge" style="display:inline-block;background:#e6efff;color:#0f1b40;padding:6px 12px;border-radius:999px;font-weight:600;letter-spacing:0.4px;font-size:12px;text-transform:uppercase;">Nuevo ticket</span>
                  <h1 class="title" style="margin:14px 0 4px;font-size:22px;letter-spacing:-0.2px;">Ticket #{code}</h1>
                  <p class="muted subtitle" style="margin:0 0 14px;color:#6b7280;font-size:14px;">{request_text}</p>
                  {f'<p style="margin:0 0 14px;color:#111827;font-size:14px;white-space:pre-line;">{sanitized_note}</p>' if sanitized_note else ''}
                  <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="border-collapse:collapse;">
                    <tr>
                      <td align="center" style="padding-top:12px;">
                        <a class="button cta" href="http://localhost:8080/tickets" target="_blank" rel="noopener noreferrer"
                           style="display:inline-block;min-width:220px;max-width:100%;background:#1565c0;color:#ffffff;text-decoration:none;padding:14px 20px;border-radius:999px;font-weight:700;letter-spacing:0.2px;text-align:center;">
                           Ver ticket
                        </a>
                      </td>
                    </tr>
                  </table>
                </td>
              </tr>
            </table>
          </td>
        </tr>
      </table>
    </body>
    </html>
    """


def build_ticket_status_email_body(code: str, status: str | None) -> str:
    """
    Plantilla para cambio de estado con pasos visuales (barra/etapas).
    """
    # Mantener el mismo orden que el selector del frontend.
    steps: list[str] = ['En espera', 'Abierto', 'En proceso', 'Resuelto', 'Cancelado']
    status_text = status or 'Actualizado'

    def normalize(text: str | None) -> str:
        return (text or '').strip().lower()

    normalized_status = normalize(status)
    active_index = next((index for index, label in enumerate(steps) if normalize(label) == normalized_status), 0)

    step_cells = ''
    for index, label in enumerate(steps):
        is_active = index == active_index
        line_color = '#1565c0' if is_active else '#d1d5db'
        circle_color = '#1565c0' if is_active else '#d1d5db'
        text_color = '#111827' if is_active else '#9ca3af'
        step_cells += f"""
          <td class="step-cell" style="padding:0 6px;width:{100//len(steps)}%;text-align:center;">
            <div class="step-line" style="height:4px;background:{line_color};border-radius:999px;margin:0 auto 8px;width:100%;max-width:120px;"></div>
            <div class="step-dot" style="margin:0 auto 6px;">
              <span style="display:inline-block;width:16px;height:16px;border-radius:999px;background:{circle_color};border:1px solid #9ca3af;"></span>
            </div>
            <div class="step-label" style="font-size:12px;font-weight:600;color:{text_color};line-height:1.3;">{label}</div>
          </td>
        """

    return f"""
    <!doctype html>
    <html>
    <head>
      <meta charset="utf-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <meta name="color-scheme" content="light">
      <meta name="supported-color-schemes" content="light">
      <style>
        :root {{ color-scheme: light; }}
        body, .email-bg {{ background:#f8fafc !important; color:#111827 !important; }}
        .card {{ background:#ffffff !important; border-radius:12px; border:1px solid #e5e7eb; overflow:hidden; }}
        .badge {{ background:#e6efff; color:#0f1b40; }}
        .muted {{ color:#6b7280; }}
        .cta {{ background:#1565c0; color:#ffffff; }}
        @media (prefers-color-scheme: dark) {{
          :root {{ color-scheme: light; }}
        }}
        @media only screen and (max-width: 520px) {{
          body.email-bg {{ padding:12px !important; }}
          .card {{ max-width:480px !important; border-radius:10px !important; }}
          .content {{ padding:14px 12px 16px !important; }}
          .title {{ font-size:20px !important; }}
          .subtitle {{ font-size:13px !important; }}
          .cta {{ width:100% !important; min-width:0 !important; display:block !important; }}
          .steps {{ margin-top:8px !important; }}
          .step-cell {{ display:block !important; width:100% !important; padding:0 0 12px 0 !important; }}
          .step-line {{ width:78% !important; margin:0 auto 8px !important; }}
          .step-label {{ font-size:12px !important; }}
        }}
      </style>
    </head>
    <body bgcolor="#f8fafc" class="email-bg" style="margin:0;padding:16px;background:#f8fafc;font-family:Roboto,'Segoe UI',Arial,sans-serif;color:#111827;">
      <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" bgcolor="#f8fafc" style="border-collapse:collapse;margin:0 auto;padding:0;background:#f8fafc;">
        <tr>
          <td align="center" style="padding:0;">
            <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" bgcolor="#ffffff" class="card" style="max-width:640px;width:100%;background:#ffffff;border-radius:12px;border:1px solid #e5e7eb;overflow:hidden;">
              <tr>
                <td style="height:6px;background:linear-gradient(90deg,#1e88e5,#1565c0);padding:0;margin:0;font-size:0;line-height:0;">&nbsp;</td>
              </tr>
              <tr>
                <td bgcolor="#ffffff" class="content" style="padding:18px 16px 20px;background:#ffffff;">
                  <span class="badge" style="display:inline-block;background:#e6efff;color:#0f1b40;padding:6px 12px;border-radius:999px;font-weight:600;letter-spacing:0.4px;font-size:12px;text-transform:uppercase;">Estado actualizado</span>
                  <h1 class="title" style="margin:14px 0 4px;font-size:22px;letter-spacing:-0.2px;">Ticket #{code}</h1>
                  <p class="muted subtitle" style="margin:0 0 14px;color:#6b7280;font-size:14px;">Estado: {status_text}</p>
                  <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" class="steps" style="border-collapse:collapse;margin-top:4px;">
                    <tr class="steps-row">
                      {step_cells}
                    </tr>
                  </table>
                  <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="border-collapse:collapse;">
                    <tr>
                      <td align="center" style="padding-top:16px;">
                        <a class="cta" href="http://localhost:8080/tickets" target="_blank" rel="noopener noreferrer"
                           style="display:inline-block;min-width:220px;max-width:100%;background:#1565c0;color:#ffffff;text-decoration:none;padding:14px 20px;border-radius:999px;font-weight:700;letter-spacing:0.2px;text-align:center;">
                           Ver ticket
                        </a>
                      </td>
                    </tr>
                  </table>
                </td>
              </tr>
            </table>
          </td>
        </tr>
      </table>
    </body>
    </html>
    """


def build_ticket_email_text(code: str, request_type: str | None, note: str | None = None) -> str:
    """
    Versión texto plano para clientes que fuerzan modo claro/oscuro.
    """
    request_text = request_type or 'Ticket'
    sanitized_note = (note or '').strip()

    lines = [
        f'Ticket #{code}',
        f'Tipo: {request_text}',
    ]
    if sanitized_note:
        lines.append(f'Nota: {sanitized_note}')

    lines.append('Ver ticket: http://localhost:8080/tickets')
    return '\n'.join(lines)


def build_ticket_status_email_text(code: str, status: str | None) -> str:
    """
    Versión texto plano del correo de estado.
    """
    status_text = status or 'Actualizado'
    return '\n'.join([
        f'Ticket #{code}',
        f'Estado: {status_text}',
        'Ver ticket: http://localhost:8080/tickets',
    ])
'''