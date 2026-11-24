
import { useState } from "react";
import "./App.css";

type Campanha = {
  id: number;
  nome: string;
  mestre: string;
  jogadores: number;
  descricao: string;
  status: "Em andamento" | "Preparação";
  cor: string;
};

const campanhas: Campanha[] = [
  {
    id: 1,
    nome: "As Crônicas de Valdoren",
    mestre: "Arthur",
    jogadores: 4,
    descricao: "Uma jornada por terras antigas, mistérios e criaturas esquecidas.",
    status: "Em andamento",
    cor: "purple",
  },
  {
    id: 2,
    nome: "A Última Chama",
    mestre: "Arthur",
    jogadores: 3,
    descricao: "Heróis precisam impedir que uma antiga profecia se cumpra.",
    status: "Preparação",
    cor: "orange",
  },
];

function Login({ onLogin }: { onLogin: () => void }) {
  const [modoCadastro, setModoCadastro] = useState(false);
  const [nome, setNome] = useState("");
  const [email, setEmail] = useState("");
  const [senha, setSenha] = useState("");
  const [mostrarSenha, setMostrarSenha] = useState(false);

  function enviarFormulario(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();

    // Login temporário: ainda não valida com o backend.
    onLogin();
  }

  return (
    <main className="login-page">
      <div className="login-background-decoration decoration-one" />
      <div className="login-background-decoration decoration-two" />

      <section className="login-panel">
        <div className="login-brand">
          <div className="login-brand-icon">⚔</div>

          <div>
            <h1>CombatForge</h1>
            <span>FORJE SUA LENDA</span>
          </div>
        </div>

        <div className="login-heading">
          <span className="login-eyebrow">
            {modoCadastro ? "COMECE SUA JORNADA" : "SEU CENTRO DE COMANDO"}
          </span>

          <h2>
            {modoCadastro ? "Crie sua conta" : "Bem-vindo de volta"}
          </h2>

          <p>
            {modoCadastro
              ? "Prepare-se para escrever sua própria lenda."
              : "Suas aventuras estão esperando por você."}
          </p>
        </div>

        <form className="login-form" onSubmit={enviarFormulario}>
          {modoCadastro && (
            <div className="login-field">
              <label htmlFor="nome">Nome de aventureiro</label>

              <input
                id="nome"
                type="text"
                placeholder="Como devemos chamar você?"
                value={nome}
                onChange={(event) => setNome(event.target.value)}
                required
              />
            </div>
          )}

          <div className="login-field">
            <label htmlFor="email">E-mail</label>

            <input
              id="email"
              type="email"
              placeholder="seu@email.com"
              value={email}
              onChange={(event) => setEmail(event.target.value)}
              required
            />
          </div>

          <div className="login-field">
            <label htmlFor="senha">Senha</label>

            <div className="password-input-wrapper">
              <input
                id="senha"
                type={mostrarSenha ? "text" : "password"}
                placeholder="Digite sua senha"
                value={senha}
                onChange={(event) => setSenha(event.target.value)}
                required
                minLength={8}
              />

              <button
                type="button"
                className="show-password-button"
                onClick={() => setMostrarSenha(!mostrarSenha)}
              >
                {mostrarSenha ? "Ocultar" : "Mostrar"}
              </button>
            </div>

            <small className="password-hint">
              A senha deve ter pelo menos 8 caracteres.
            </small>
          </div>

          {!modoCadastro && (
            <div className="login-options">
              <label className="remember-option">
                <input type="checkbox" />
                <span>Manter conectado</span>
              </label>

              <button
                type="button"
                className="forgot-password-button"
                onClick={() =>
                  alert("A recuperação de senha será implementada depois.")
                }
              >
                Esqueceu a senha?
              </button>
            </div>
          )}

          <button type="submit" className="login-submit-button">
            {modoCadastro ? "Criar conta" : "Entrar"}
            <span>→</span>
          </button>
        </form>

        <div className="login-switch">
          <span>
            {modoCadastro
              ? "Já possui uma conta?"
              : "Ainda não tem uma conta?"}
          </span>

          <button
            type="button"
            onClick={() => setModoCadastro(!modoCadastro)}
          >
            {modoCadastro ? "Entrar" : "Criar conta"}
          </button>
        </div>

        <div className="login-divider">
          <span>✦</span>
        </div>

        <p className="login-footer">
          Que suas histórias sejam lendárias.
        </p>
      </section>

      <footer className="login-bottom">
        <span>COMBATFORGE</span>
        <span>UM MUNDO DE AVENTURAS</span>
      </footer>
    </main>
  );
}

function Dashboard({ onLogout }: { onLogout: () => void }) {
  const [pagina, setPagina] = useState("Visão geral");
  const [busca, setBusca] = useState("");

  const campanhasFiltradas = campanhas.filter((campanha) =>
    campanha.nome.toLowerCase().includes(busca.toLowerCase()),
  );

  const menu = [
    { nome: "Visão geral", simbolo: "⌂" },
    { nome: "Minhas campanhas", simbolo: "⚔" },
    { nome: "Personagens", simbolo: "♙" },
    { nome: "Criaturas", simbolo: "♜" },
  ];

  return (
    <div className="app">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-icon">⚔</div>
          <div>
            <h1>CombatForge</h1>
            <span>FORJE SUA LENDA</span>
          </div>
        </div>

        <div className="menu-label">MENU PRINCIPAL</div>

        <nav className="navigation">
          {menu.map((item) => (
            <button
              key={item.nome}
              className={`nav-item ${pagina === item.nome ? "active" : ""}`}
              onClick={() => setPagina(item.nome)}
            >
              <span className="nav-symbol">{item.simbolo}</span>
              {item.nome}
            </button>
          ))}
        </nav>

        <div className="sidebar-bottom">
          <div className="user-card">
            <div className="avatar">A</div>

            <div className="user-info">
              <strong>Arthur</strong>
              <span>Mestre de RPG</span>
            </div>

            <button
              className="user-menu"
              title="Sair"
              onClick={onLogout}
            >
              ↪
            </button>
          </div>
        </div>
      </aside>

      <main className="main-content">
        <header className="topbar">
          <div className="breadcrumb">
            <span>CombatForge</span>
            <span className="breadcrumb-separator">/</span>
            <strong>{pagina}</strong>
          </div>

          <div className="topbar-right">
            <span className="online-status">
              <span className="status-dot" />
              Sistema online
            </span>

            <div className="top-avatar">A</div>
          </div>
        </header>

        <section className="page-content">
          <div className="welcome-section">
            <div>
              <div className="eyebrow">SEU CENTRO DE COMANDO</div>
              <h2>Bem-vindo de volta, Arthur</h2>
              <p>
                Prepare suas aventuras. Suas próximas lendas começam aqui.
              </p>
            </div>

            <button className="primary-button">
              <span>＋</span> Criar campanha
            </button>
          </div>

          <div className="stats-grid">
            <div className="stat-card">
              <div className="stat-icon purple-icon">⚔</div>
              <div className="stat-info">
                <span>Campanhas</span>
                <strong>2</strong>
                <small>Suas aventuras</small>
              </div>
            </div>

            <div className="stat-card">
              <div className="stat-icon blue-icon">♙</div>
              <div className="stat-info">
                <span>Personagens</span>
                <strong>7</strong>
                <small>Heróis registrados</small>
              </div>
            </div>

            <div className="stat-card">
              <div className="stat-icon orange-icon">♜</div>
              <div className="stat-info">
                <span>Criaturas</span>
                <strong>12</strong>
                <small>Em seu bestiário</small>
              </div>
            </div>
          </div>

          <section className="campaign-section">
            <div className="section-heading">
              <div>
                <h3>Suas campanhas</h3>
                <p>Continue de onde suas aventuras pararam.</p>
              </div>

              <div className="campaign-actions">
                <div className="search-box">
                  <span>⌕</span>
                  <input
                    type="text"
                    placeholder="Buscar campanha..."
                    value={busca}
                    onChange={(event) => setBusca(event.target.value)}
                  />
                </div>

                <button className="secondary-button">Ver todas ↗</button>
              </div>
            </div>

            <div className="campaign-grid">
              {campanhasFiltradas.map((campanha) => (
                <article className="campaign-card" key={campanha.id}>
                  <div className={`campaign-banner ${campanha.cor}`}>
                    <div className="banner-symbol">✦</div>
                    <span className="banner-label">D&D 5ª EDIÇÃO</span>
                    <div className="banner-decoration">✧</div>
                  </div>

                  <div className="campaign-card-content">
                    <div className="campaign-title-row">
                      <h4>{campanha.nome}</h4>

                      <span
                        className={`campaign-status ${
                          campanha.status === "Em andamento"
                            ? "status-active"
                            : "status-preparing"
                        }`}
                      >
                        {campanha.status}
                      </span>
                    </div>

                    <p className="campaign-description">
                      {campanha.descricao}
                    </p>

                    <div className="campaign-meta">
                      <span>♙ {campanha.jogadores} jogadores</span>
                      <span>♛ Mestre: {campanha.mestre}</span>
                    </div>

                    <button className="campaign-button">
                      Abrir campanha <span>→</span>
                    </button>
                  </div>
                </article>
              ))}

              {campanhasFiltradas.length === 0 && (
                <div className="empty-state">
                  Nenhuma campanha encontrada.
                </div>
              )}

              <button className="new-campaign-card">
                <span className="new-campaign-icon">＋</span>
                <strong>Iniciar uma nova aventura</strong>
                <span>Crie uma campanha e reúna seu grupo.</span>
              </button>
            </div>
          </section>

          <footer className="page-footer">
            <span>COMBATFORGE</span>
            <span>Que suas histórias sejam lendárias.</span>
          </footer>
        </section>
      </main>
    </div>
  );
}

function App() {
  const [logado, setLogado] = useState(false);

  if (!logado) {
    return <Login onLogin={() => setLogado(true)} />;
  }

  return <Dashboard onLogout={() => setLogado(false)} />;
}

export default App;
