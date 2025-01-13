"""empty message

Revision ID: 67ec05a773b7
Revises: 
Create Date: 2025-01-13 18:41:57.556642

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '67ec05a773b7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('categorias',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('categoria', sa.String(length=120), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('categoria')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user', sa.String(length=120), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password', sa.String(length=80), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('comentarios',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('fecha_creacion', sa.DateTime(), nullable=False),
    sa.Column('comentario', sa.Text(), nullable=True),
    sa.Column('tipo', sa.String(length=120), nullable=False),
    sa.Column('to_id', sa.Integer(), nullable=False),
    sa.Column('from_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['from_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['to_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('rutas',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('titulo', sa.String(length=120), nullable=False),
    sa.Column('detalles', sa.JSON(), nullable=True),
    sa.Column('usuario_id', sa.Integer(), nullable=True),
    sa.Column('category_id', sa.Integer(), nullable=True),
    sa.Column('fecha_creada', sa.Date(), nullable=False),
    sa.Column('fecha_inicio', sa.Date(), nullable=False),
    sa.ForeignKeyConstraint(['category_id'], ['categorias.id'], ),
    sa.ForeignKeyConstraint(['usuario_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('titulo')
    )
    op.create_table('eventos',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('titulo', sa.String(length=120), nullable=False),
    sa.Column('detalles', sa.JSON(), nullable=True),
    sa.Column('tipo', sa.String(length=120), nullable=False),
    sa.Column('fecha', sa.Date(), nullable=False),
    sa.Column('category_id', sa.Integer(), nullable=False),
    sa.Column('rutas_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['category_id'], ['categorias.id'], ),
    sa.ForeignKeyConstraint(['rutas_id'], ['rutas.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('titulo')
    )
    op.create_table('valoraciones',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('valoracion', sa.Float(), nullable=True),
    sa.Column('tipo', sa.String(length=120), nullable=False),
    sa.Column('to_id', sa.Integer(), nullable=False),
    sa.Column('from_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['from_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['to_id'], ['rutas.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('favorites',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('rutas_id', sa.Integer(), nullable=True),
    sa.Column('eventos_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['eventos_id'], ['eventos.id'], ),
    sa.ForeignKeyConstraint(['rutas_id'], ['rutas.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('rutas_eventos',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('ruta_id', sa.Integer(), nullable=False),
    sa.Column('evento_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['evento_id'], ['eventos.id'], ),
    sa.ForeignKeyConstraint(['ruta_id'], ['rutas.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('rutas_eventos')
    op.drop_table('favorites')
    op.drop_table('valoraciones')
    op.drop_table('eventos')
    op.drop_table('rutas')
    op.drop_table('comentarios')
    op.drop_table('users')
    op.drop_table('categorias')
    # ### end Alembic commands ###
