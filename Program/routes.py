from .init import app, db, login_manager
from flask import Flask, request, render_template, url_for, redirect, flash
from flask_login import login_user, logout_user, current_user, login_required
from .forms import registro, CalculoFerroviario, CalculoVelocidade, CalculoTrilho
from .models import User



@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    form = CalculoFerroviario()
    resultados = None
    
    if form.validate_on_submit():
        V = form.velocidade.data
        R = form.raio.data
        b = form.bitola.data
        Lb = form.largura_boleto.data
        H = form.altura_cg.data
        eta = form.coef_seguranca.data
        d = form.deslocamento_cg.data
        Jc = form.aceleracao_jc.data
        g = form.gravidade.data

        B = b + Lb

        
        h_teorica = (B * (V ** 2)) / (127 * R)

        termo_seguranca = (B / (H * eta)) * ((B / 2) - d)

        h_seguranca = h_teorica - termo_seguranca

        h_seguranca_parado = termo_seguranca

        h_conforto = h_teorica - ((Jc * B) / g)

        resultados = {
            "h_teorica": round(h_teorica, 4),
            "h_seguranca": round(h_seguranca, 4),
            "h_seguranca_parado": round(h_seguranca_parado, 4),
            "h_conforto": round(h_conforto, 4),
            "unidade": "metros"
        }

    return render_template("home.html", form=form, resultados=resultados)

@app.route('/programa', methods=['GET', 'POST'])
@login_required
def programa():
    form = CalculoVelocidade()
    resultados = None
    
    if form.validate_on_submit():
        R = form.raio.data
        h = form.superelevacao.data
        b = form.bitola.data
        Lb = form.largura_boleto.data
        V_input = form.velocidade.data 
        H = form.altura_cg.data
        eta = form.coef_seguranca.data
        d = form.deslocamento_cg.data
        Jc = form.aceleracao_jc.data
        g = form.gravidade.data

        B = b + Lb

        termo_seguranca = (B / 2 - d) / (H * eta)
        V_max_seguranca = (127 * (h / B + termo_seguranca))**0.5 * (R**0.5)

        termo_conforto = (Jc * B) / g
        V_max_conforto = (127 * ((h + termo_conforto) / B))**0.5 * (R**0.5)

        val_interno_min = 127 * (h / B - termo_seguranca)
        if val_interno_min < 0:
            V_min = 0 
        else:
            V_min = val_interno_min**0.5 * (R**0.5)


        R_min_seg = (V_input**2) / (127 * (h/B + termo_seguranca))
        
        R_min_conf = (V_input**2) / (127 * (Jc/g + h/B))
        
        R_min_final = max(R_min_seg, R_min_conf)

        if R >= 500:
            S = 0
        else:
            S = (6 / R) - 0.012
            if S > 0.02:
                S = 0.02
            if S < 0:
                S = 0
        
        resultados = {
            "v_max_seg": round(V_max_seguranca, 2),
            "v_max_conf": round(V_max_conforto, 2),
            "v_min": round(V_min, 2),
            "r_min": round(R_min_final, 2),
            "superlargura_mm": round(S * 1000, 1) 
        }

    return render_template("programa.html", form=form, resultados=resultados)

@app.route('/trilho', methods=['GET', 'POST'])
@login_required
def trilho():
    form = CalculoTrilho()
    resultados = None
    
    if form.validate_on_submit():
        Pe = form.carga_por_eixo.data
        V = form.velocidade.data
        a = form.espacamento_dormente.data
        b = form.largura_dormente.data
        C = form.coef_lastro.data
        E = form.modulo_elasticidade.data
        I = form.momento_inercia.data
        W = form.modulo_resistencia.data
        sigma_adm = form.tensao_admissivel.data

        P = Pe / 2

        Cd_calc = 1 + (V**2 / 30000)
        
        if Cd_calc < 1.4:
            Cd = 1.4
            msg_cd = "Adotado mínimo normativo (1.4)"
        else:
            Cd = Cd_calc
            msg_cd = "Adotado valor calculado"

        M_winkler = 0.1875 * P * Cd * a

        D = 0.9 * C * b * a
        gamma = (6 * E * I) / (D * (a**3))

        term_h1 = (7 + 8 * gamma) / (8 * (5 + 2 * gamma))
        M_zim_1 = term_h1 * P * Cd * a

        term_h2 = gamma / (2 + 3 * gamma)
        M_zim_2 = term_h2 * P * Cd * a

        M_zim_max = max(M_zim_1, M_zim_2)
        M_projeto = max(M_winkler, M_zim_max)

        sigma_trabalho = M_projeto / W
        
        status = "APROVADO" if sigma_trabalho < sigma_adm else "REPROVADO"
        css_class = "text-success" if sigma_trabalho < sigma_adm else "text-danger"

        resultados = {
            "P": P,
            "Cd": round(Cd, 3),
            "Cd_calc": round(Cd_calc, 3),  
            "msg_cd": msg_cd,             
            "gamma": round(gamma, 3),
            "M_winkler": round(M_winkler, 2),
            "M_zim": round(M_zim_max, 2),
            "sigma_calc": round(sigma_trabalho, 2),
            "status": status,
            "css_class": css_class
        }

    return render_template("trilho.html", form=form, resultados=resultados)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = registro()
    if form.validate_on_submit():

        if db.session.query(User).filter_by(email=form.email.data).first():
            flash("Esse email já existe!")
            return render_template("register.html", form=form)
        
        user_to_create = User(name = form.name.data,
                              email = form.email.data,
                              password = form.password1.data
        )

        db.session.add(user_to_create)
        db.session.commit()
        db.create_all()
        
         
        return redirect(url_for('home'))
    return render_template("register.html", form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        user_email = request.form['email']
        user_password = request.form['password']

        user_data = User.query.filter_by(email=user_email).first()
        if user_data and user_data.check_password_correction(user_password):

            login_user(user_data)
            flash('Você está logado!')
            return redirect(url_for('home'))
        else:
            flash('Login inválido ou senha incorreta!')     
    
    return render_template("login.html")

@app.route('/logout')
def logout():
    logout_user()
    flash('Você saiu do programa!', category='info')
    return redirect(url_for("login"))


