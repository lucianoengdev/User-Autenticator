from .init import app, db, login_manager
from flask import Flask, request, render_template, url_for, redirect, flash
from flask_login import login_user, logout_user, current_user, login_required
from .forms import registro, CalculoFerroviario, CalculoVelocidade, CalculoTrilho, CalculoDormente, CalculoLastro
from .models import User



@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    form = CalculoFerroviario()
    resultados = None
    memoria = []
    
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
        memoria.append(f"1. Superelevação Teórica (Equilíbrio): h = (B * V²) / (127 * R)")
        memoria.append(f"   h = ({B:.2f} * {V:.2f}²) / (127 * {R:.2f}) = {h_teorica:.4f} m")

        termo_seguranca = (B / (H * eta)) * ((B / 2) - d)
        memoria.append(f"2. Termo de Segurança: T = (B / (H * η)) * ((B / 2) - d)")
        memoria.append(f"   T = ({B:.2f} / ({H:.2f} * {eta})) * (({B:.2f} / 2) - {d}) = {termo_seguranca:.4f} m")

        h_seguranca = h_teorica - termo_seguranca
        memoria.append(f"3. h Máx (Segurança Movimento): h_teo - T = {h_teorica:.4f} - {termo_seguranca:.4f} = {h_seguranca:.4f} m")

        h_seguranca_parado = termo_seguranca
        memoria.append(f"4. h Máx (Segurança Parado): T = {h_seguranca_parado:.4f} m")

        h_conforto = h_teorica - ((Jc * B) / g)
        memoria.append(f"5. h Máx (Conforto): h_teo - ((Jc * B) / g)")
        memoria.append(f"   h_conf = {h_teorica:.4f} - (({Jc} * {B:.2f}) / {g}) = {h_conforto:.4f} m")

        resultados = {
            "h_teorica": round(h_teorica, 4),
            "h_seguranca": round(h_seguranca, 4),
            "h_seguranca_parado": round(h_seguranca_parado, 4),
            "h_conforto": round(h_conforto, 4),
            "unidade": "metros"
        }

    # Passamos 'memoria' para o template
    return render_template("home.html", form=form, resultados=resultados, memoria=memoria)

@app.route('/programa', methods=['GET', 'POST'])
@login_required
def programa():
    form = CalculoVelocidade()
    resultados = None
    memoria = []
    
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
        memoria.append(f"1. V.Máx (Segurança): √[127 * (h/B + T_seg) * R]")
        memoria.append(f"   V_seg = {V_max_seguranca:.2f} km/h")

        termo_conforto = (Jc * B) / g
        V_max_conforto = (127 * ((h + termo_conforto) / B))**0.5 * (R**0.5)
        memoria.append(f"2. V.Máx (Conforto): √[127 * ((h + T_conf)/B) * R]")
        memoria.append(f"   V_conf = {V_max_conforto:.2f} km/h")

        val_interno_min = 127 * (h / B - termo_seguranca)
        if val_interno_min < 0:
            V_min = 0 
        else:
            V_min = val_interno_min**0.5 * (R**0.5)
        memoria.append(f"3. V.Mín (Tombamento Interno): {V_min:.2f} km/h")

        R_min_seg = (V_input**2) / (127 * (h/B + termo_seguranca))
        R_min_conf = (V_input**2) / (127 * (Jc/g + h/B))
        R_min_final = max(R_min_seg, R_min_conf)
        memoria.append(f"4. Raio Mínimo (Para V={V_input}): Max({R_min_seg:.1f}, {R_min_conf:.1f}) = {R_min_final:.2f} m")

        if R >= 500:
            S = 0
            memoria.append("5. Superlargura: R >= 500m, logo S = 0")
        else:
            S = (6 / R) - 0.012
            if S > 0.02: S = 0.02
            if S < 0: S = 0
            memoria.append(f"5. Superlargura: Calculado = {(6/R - 0.012)*1000:.1f}mm (Limitado entre 0 e 20mm)")
        
        resultados = {
            "v_max_seg": round(V_max_seguranca, 2),
            "v_max_conf": round(V_max_conforto, 2),
            "v_min": round(V_min, 2),
            "r_min": round(R_min_final, 2),
            "superlargura_mm": round(S * 1000, 1) 
        }

    return render_template("programa.html", form=form, resultados=resultados, memoria=memoria)

@app.route('/trilho', methods=['GET', 'POST'])
@login_required
def trilho():
    form = CalculoTrilho()
    resultados = None
    memoria = []
    
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
        memoria.append(f"1. Carga por Roda (P): {Pe}/2 = {P} kgf")

        Cd_calc = 1 + (V**2 / 30000)
        Cd = max(1.4, Cd_calc)
        msg_cd = "Mínimo (1.4)" if Cd == 1.4 else "Calculado"
        memoria.append(f"2. Coef. Dinâmico (Cd): 1 + ({V}²/30000) = {Cd_calc:.3f} -> Adotado: {Cd} ({msg_cd})")

        M_winkler = 0.1875 * P * Cd * a
        memoria.append(f"3. Momento Winkler: 0.1875 * P * Cd * a = {M_winkler:.2f} kgf.cm")

        D = 0.9 * C * b * a
        gamma = (6 * E * I) / (D * (a**3))
        memoria.append(f"4. Zimmermann: D={D:.1f}, Gama={gamma:.3f}")

        term_h1 = (7 + 8 * gamma) / (8 * (5 + 2 * gamma))
        M_zim_1 = term_h1 * P * Cd * a
        
        term_h2 = gamma / (2 + 3 * gamma)
        M_zim_2 = term_h2 * P * Cd * a

        M_zim_max = max(M_zim_1, M_zim_2)
        memoria.append(f"5. Momento Zimmermann: Max(Hip1: {M_zim_1:.1f}, Hip2: {M_zim_2:.1f}) = {M_zim_max:.2f} kgf.cm")

        M_projeto = max(M_winkler, M_zim_max)
        sigma_trabalho = M_projeto / W
        memoria.append(f"6. Tensão de Trabalho: M_proj / W = {M_projeto:.1f} / {W} = {sigma_trabalho:.2f} kgf/cm²")

        status = "APROVADO" if sigma_trabalho < sigma_adm else "REPROVADO"
        css_class = "text-success" if sigma_trabalho < sigma_adm else "text-danger"

        resultados = {
            "P": P, "Cd": round(Cd, 3), "Cd_calc": round(Cd_calc, 3), "msg_cd": msg_cd,
            "gamma": round(gamma, 3), "M_winkler": round(M_winkler, 2), "M_zim": round(M_zim_max, 2),
            "sigma_calc": round(sigma_trabalho, 2), "status": status, "css_class": css_class
        }

    return render_template("trilho.html", form=form, resultados=resultados, memoria=memoria)

@app.route('/dormente', methods=['GET', 'POST'])
@login_required
def dormente():
    form = CalculoDormente()
    resultados = None
    memoria = []
    
    if form.validate_on_submit():
        Pe = form.carga_por_eixo.data
        V = form.velocidade.data
        d_veiculo = form.distancia_eixos_veiculo.data 
        taxa = form.taxa_dormentacao.data
        B = form.distancia_eixo_trilhos.data
        y = form.largura_placa.data
        L = form.comprimento_dormente.data
        b = form.largura_dormente.data
        t = form.altura_dormente.data 
        sigma_adm = form.tensao_admissivel.data

        a = 100000 / taxa
        memoria.append(f"1. Espaçamento (a): 100000 / {taxa} = {a:.2f} cm")

        Pr = Pe / 2
        
        Cd_calc = 1 + (V**2 / 30000)
        Cd = max(1.4, Cd_calc)
        msg_cd = "Mínimo" if Cd == 1.4 else "Calculado"
        memoria.append(f"2. Coef. Dinâmico: {Cd:.3f} ({msg_cd})")

        fator_distribuicao = d_veiculo / a
        P_dormente = (Pr / fator_distribuicao) * Cd
        memoria.append(f"3. Carga no Dormente (P): (Pr / (d/a)) * Cd = ({Pr} / ({d_veiculo}/{a:.1f})) * {Cd:.2f} = {P_dormente:.2f} kgf")

        M_max = (P_dormente / 8) * (L - B - y)
        memoria.append(f"4. Momento Máx: (P/8)*(L-B-y) = {M_max:.2f} kgf.cm")

        W = (b * (t**2)) / 6
        memoria.append(f"5. Módulo Resistente (W): (b*t²)/6 = {W:.2f} cm³")

        sigma = M_max / W
        memoria.append(f"6. Tensão Atuante: M/W = {sigma:.2f} kgf/cm²")

        status = "APROVADO" if sigma < sigma_adm else "REPROVADO"
        css_class = "text-success" if sigma < sigma_adm else "text-danger"

        resultados = {
            "a": round(a, 1), "Cd": round(Cd, 3), "Cd_calc": round(Cd_calc, 3), "msg_cd": msg_cd,
            "P_dormente": round(P_dormente, 2), "M_max": round(M_max, 2), "W": round(W, 2),
            "sigma": round(sigma, 2), "status": status, "css_class": css_class
        }

    return render_template("dormente.html", form=form, resultados=resultados, memoria=memoria)

@app.route('/lastro', methods=['GET', 'POST'])
@login_required
def lastro():
    form = CalculoLastro()
    resultados = None
    grafico_data = None
    memoria = []

    if form.validate_on_submit():
        Pe = form.carga_por_eixo.data
        V = form.velocidade.data
        d = form.distancia_eixos_veiculo.data
        taxa = form.taxa_dormentacao.data
        b = form.largura_dormente.data
        fs = form.faixa_socaria.data
        sigma_adm = form.tensao_admissivel.data

        a = 100000 / taxa
        Pr = Pe / 2
        Cd_calc = 1 + (V**2 / 30000)
        Cd = max(Cd_calc, 1.4)
        
        fator_distribuicao = d / a
        P_dormente = (Pr / fator_distribuicao) * Cd
        memoria.append(f"1. Carga no Dormente (P): {P_dormente:.2f} kgf")

        area_contato = b * fs
        sigma_0 = P_dormente / area_contato
        memoria.append(f"2. Pressão Contato (σ0): P / Area = {P_dormente:.1f} / ({b}*{fs}) = {sigma_0:.2f} kgf/cm²")

        if sigma_adm <= 0: sigma_adm = 1.0 

        h_calc = (16.8 * sigma_0 / sigma_adm) ** 0.8
        memoria.append(f"3. Altura Talbot (h): (16.8 * σ0 / σ_adm)^0.8")
        memoria.append(f"   h = (16.8 * {sigma_0:.2f} / {sigma_adm})^0.8 = {h_calc:.2f} cm")

        h_final = round(h_calc, 1)

        # ... (Lógica do Gráfico Mantida) ...
        labels_z = []
        values_sigma = []
        limit_line = []
        profundidade_max = int(h_final) + 30
        for z in range(5, profundidade_max, 5):
            s_z = (16.8 * sigma_0) / (z ** 1.25)
            labels_z.append(z)
            values_sigma.append(round(s_z, 2))
            limit_line.append(sigma_adm)

        resultados = {
            "a": round(a, 1), "P_dormente": round(P_dormente, 0), "area_contato": round(area_contato, 0),
            "sigma_0": round(sigma_0, 2), "h_calc": h_final, "sigma_adm": sigma_adm
        }

        grafico_data = {
            "labels": labels_z, "data_sigma": values_sigma, "data_limit": limit_line
        }

    return render_template("lastro.html", form=form, resultados=resultados, grafico=grafico_data, memoria=memoria)

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


