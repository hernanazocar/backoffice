/**
 * Módulo de Posts de Marketing para el Dashboard
 * Se integra automáticamente al dashboard existente
 */

const MarketingPosts = {
  API_URL: 'http://localhost:5000/api/marketing',

  init() {
    console.log('📢 Inicializando módulo de Marketing Posts...');
    this.injectStyles();
    this.injectHTML();
    this.loadPosts();
    this.startAutoRefresh();
  },

  injectStyles() {
    const styles = `
      <style>
        .posts-section {
          background: white;
          border-radius: 14px;
          padding: 20px;
          margin-bottom: 8px;
          box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        }

        .posts-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 16px;
        }

        .posts-title {
          font-size: 16px;
          font-weight: 700;
          display: flex;
          align-items: center;
          gap: 8px;
        }

        .posts-badge {
          background: #ff6b35;
          color: white;
          padding: 2px 8px;
          border-radius: 12px;
          font-size: 11px;
          font-weight: 600;
        }

        .posts-grid {
          display: grid;
          grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
          gap: 16px;
        }

        .post-card {
          background: #fafbfc;
          border: 1px solid #e8eaed;
          border-radius: 12px;
          overflow: hidden;
          transition: all 0.3s ease;
        }

        .post-card:hover {
          box-shadow: 0 4px 12px rgba(0,0,0,0.1);
          transform: translateY(-2px);
        }

        .post-image {
          width: 100%;
          height: 200px;
          object-fit: cover;
          background: linear-gradient(135deg, #ff6b35, #ec4899);
          display: flex;
          align-items: center;
          justify-content: center;
          color: white;
          font-size: 14px;
        }

        .post-image img {
          width: 100%;
          height: 100%;
          object-fit: cover;
        }

        .post-content {
          padding: 16px;
        }

        .post-copy {
          font-size: 13px;
          line-height: 1.5;
          color: #1a1a1a;
          margin-bottom: 12px;
          max-height: 80px;
          overflow: hidden;
          display: -webkit-box;
          -webkit-line-clamp: 4;
          -webkit-box-orient: vertical;
        }

        .post-meta {
          display: flex;
          gap: 12px;
          margin-bottom: 12px;
          flex-wrap: wrap;
        }

        .post-meta-item {
          display: flex;
          align-items: center;
          gap: 4px;
          font-size: 11px;
          color: #6e7781;
        }

        .post-hashtags {
          display: flex;
          gap: 6px;
          flex-wrap: wrap;
          margin-bottom: 12px;
        }

        .hashtag {
          background: #e2e8f0;
          color: #475569;
          padding: 4px 8px;
          border-radius: 6px;
          font-size: 10px;
          font-weight: 600;
        }

        .post-actions {
          display: flex;
          gap: 8px;
        }

        .post-btn {
          flex: 1;
          padding: 10px;
          border: none;
          border-radius: 8px;
          font-size: 12px;
          font-weight: 600;
          cursor: pointer;
          transition: all 0.2s ease;
          display: flex;
          align-items: center;
          justify-content: center;
          gap: 4px;
        }

        .post-btn-approve {
          background: #22c55e;
          color: white;
        }

        .post-btn-approve:hover {
          background: #16a34a;
        }

        .post-btn-edit {
          background: #3b82f6;
          color: white;
        }

        .post-btn-edit:hover {
          background: #2563eb;
        }

        .post-btn-reject {
          background: #ef4444;
          color: white;
        }

        .post-btn-reject:hover {
          background: #dc2626;
        }

        .post-btn:disabled {
          opacity: 0.5;
          cursor: not-allowed;
        }

        .no-posts {
          text-align: center;
          padding: 40px;
          color: #6e7781;
        }

        .loading {
          text-align: center;
          padding: 40px;
          color: #6e7781;
        }

        .platform-badge {
          display: inline-flex;
          align-items: center;
          gap: 4px;
          padding: 4px 8px;
          background: #e8eaed;
          border-radius: 6px;
          font-size: 10px;
          font-weight: 600;
          color: #1a1a1a;
        }

        .platform-instagram { background: #fce4ec; color: #e91e63; }
        .platform-facebook { background: #e3f2fd; color: #1976d2; }
        .platform-linkedin { background: #e1f5fe; color: #0277bd; }
      </style>
    `;

    document.head.insertAdjacentHTML('beforeend', styles);
  },

  injectHTML() {
    const html = `
      <div class="posts-section" id="marketing-posts-section">
        <div class="posts-header">
          <div class="posts-title">
            📋 Posts Pendientes de Aprobación
            <span class="posts-badge" id="posts-count">0</span>
          </div>
          <button onclick="MarketingPosts.loadPosts()" style="padding: 6px 12px; background: #f1f5f9; border: none; border-radius: 6px; cursor: pointer; font-size: 11px; font-weight: 600;">
            🔄 Actualizar
          </button>
        </div>
        <div id="posts-container" class="loading">
          Cargando posts...
        </div>
      </div>
    `;

    // Insertar antes de bottom-panels
    const bottomPanels = document.querySelector('.bottom-panels');
    if (bottomPanels) {
      bottomPanels.insertAdjacentHTML('beforebegin', html);
    }
  },

  async loadPosts() {
    try {
      const response = await fetch(`${this.API_URL}/posts/pending`);
      const data = await response.json();

      if (data.success) {
        this.renderPosts(data.posts);
        document.getElementById('posts-count').textContent = data.count;
      } else {
        this.showError('Error cargando posts');
      }
    } catch (error) {
      console.error('Error:', error);
      this.showError('No se pudo conectar con la API. ¿Está corriendo en localhost:5000?');
    }
  },

  renderPosts(posts) {
    const container = document.getElementById('posts-container');

    if (posts.length === 0) {
      container.innerHTML = `
        <div class="no-posts">
          <div style="font-size: 48px; margin-bottom: 12px;">✅</div>
          <div style="font-size: 14px; font-weight: 600; margin-bottom: 4px;">No hay posts pendientes</div>
          <div style="font-size: 12px;">Todos los posts han sido revisados</div>
        </div>
      `;
      return;
    }

    container.className = 'posts-grid';
    container.innerHTML = posts.map(post => this.renderPostCard(post)).join('');
  },

  renderPostCard(post) {
    const platforms = post.platforms || ['instagram'];
    const platformBadges = platforms.map(p =>
      `<span class="platform-badge platform-${p}">${this.getPlatformIcon(p)} ${p}</span>`
    ).join('');

    const hashtags = post.hashtags || [];
    const hashtagsHTML = hashtags.map(tag =>
      `<span class="hashtag">#${tag}</span>`
    ).join('');

    const scheduleTime = post.schedule_time ?
      new Date(post.schedule_time).toLocaleString('es-CL', {
        weekday: 'short',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      }) : 'Ahora';

    return `
      <div class="post-card" data-post-id="${post.post_id}">
        <div class="post-image">
          ${post.image_url ?
            `<img src="${post.image_url}" alt="Post image" />` :
            '🎨 Diseño pendiente'
          }
        </div>
        <div class="post-content">
          <div class="post-copy">${post.copy || 'Sin copy'}</div>

          <div class="post-meta">
            ${platformBadges}
            <span class="post-meta-item">
              🕐 ${scheduleTime}
            </span>
          </div>

          ${hashtags.length > 0 ? `
            <div class="post-hashtags">
              ${hashtagsHTML}
            </div>
          ` : ''}

          <div class="post-actions">
            <button class="post-btn post-btn-approve" onclick="MarketingPosts.approvePost('${post.post_id}')">
              ✅ Aprobar
            </button>
            <button class="post-btn post-btn-reject" onclick="MarketingPosts.rejectPost('${post.post_id}')">
              ❌ Rechazar
            </button>
          </div>
        </div>
      </div>
    `;
  },

  getPlatformIcon(platform) {
    const icons = {
      instagram: '📷',
      facebook: '👥',
      linkedin: '💼',
      twitter: '🐦'
    };
    return icons[platform] || '📱';
  },

  async approvePost(postId) {
    if (!confirm('¿Aprobar y publicar este post?')) return;

    const card = document.querySelector(`[data-post-id="${postId}"]`);
    const approveBtn = card.querySelector('.post-btn-approve');

    approveBtn.disabled = true;
    approveBtn.textContent = '⏳ Publicando...';

    try {
      const response = await fetch(`${this.API_URL}/posts/${postId}/approve`, {
        method: 'POST'
      });

      const data = await response.json();

      if (data.success) {
        card.style.opacity = '0';
        setTimeout(() => {
          this.loadPosts();
          alert('✅ Post publicado exitosamente!');
        }, 300);
      } else {
        alert(`❌ Error: ${data.error}`);
        approveBtn.disabled = false;
        approveBtn.textContent = '✅ Aprobar';
      }
    } catch (error) {
      alert('❌ Error de conexión con la API');
      approveBtn.disabled = false;
      approveBtn.textContent = '✅ Aprobar';
    }
  },

  async rejectPost(postId) {
    const reason = prompt('¿Por qué rechazas este post? (opcional)');
    if (reason === null) return; // Usuario canceló

    const card = document.querySelector(`[data-post-id="${postId}"]`);

    try {
      const response = await fetch(`${this.API_URL}/posts/${postId}/reject`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ reason })
      });

      const data = await response.json();

      if (data.success) {
        card.style.opacity = '0';
        setTimeout(() => {
          this.loadPosts();
        }, 300);
      } else {
        alert(`❌ Error: ${data.error}`);
      }
    } catch (error) {
      alert('❌ Error de conexión con la API');
    }
  },

  showError(message) {
    const container = document.getElementById('posts-container');
    container.innerHTML = `
      <div class="no-posts">
        <div style="font-size: 48px; margin-bottom: 12px;">⚠️</div>
        <div style="font-size: 14px; font-weight: 600; margin-bottom: 4px;">Error</div>
        <div style="font-size: 12px;">${message}</div>
      </div>
    `;
  },

  startAutoRefresh() {
    // Auto-refresh cada 30 segundos
    setInterval(() => {
      this.loadPosts();
    }, 30000);
  }
};

// Auto-inicializar cuando el DOM esté listo
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => MarketingPosts.init());
} else {
  MarketingPosts.init();
}
