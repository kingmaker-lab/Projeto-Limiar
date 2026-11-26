require "digest"
require "json"
require "open3"
require "tempfile"

class Witness
  VERSION = 1
  MAX_ANCHOR_BYTES = 4096

  def initialize(anchor)
    @anchor = File.expand_path(anchor)
  end

  def run(mode, database, key)
    File.open("#{@anchor}.lock", File::RDWR | File::CREAT, 0o600) do |lock|
      lock.flock(File::LOCK_EX)
      previous = load_anchor
      case mode
      when "init"
        raise "âncora já existe" if previous
      when "verify", "advance"
        raise "âncora ausente" unless previous
      else
        raise "modo inválido"
      end
      report = inspect_history(database, key, previous)
      publish(report) if mode != "verify"
      report
    end
  end

  private

  def load_anchor
    data = File.read(@anchor, MAX_ANCHOR_BYTES + 1)
    raise "âncora excede o tamanho permitido" if data.bytesize > MAX_ANCHOR_BYTES

    value = JSON.parse(data)
    unless value.is_a?(Hash) && value.keys.sort == %w[digest generation version] &&
           value["version"] == VERSION && value["generation"].is_a?(Integer) &&
           value["generation"].between?(0, (1 << 63) - 1) &&
           value["digest"].is_a?(String) && /\A[0-9a-f]{64}\z/.match?(value["digest"])
      raise "âncora inválida"
    end
    value
  rescue Errno::ENOENT
    nil
  end

  def inspect_history(database, key, previous)
    digest = Digest::SHA256.new
    digest.update("cerberus-history-v1\0")
    generation = -1
    matched = previous.nil?
    args = ["python3", "-m", "cerberus.history_export", File.expand_path(database),
            File.expand_path(key)]
    status = Open3.popen2(*args, chdir: File.expand_path("..", __dir__)) do |input, output, child|
      input.close
      output.each_line do |line|
        generation += 1
        revision = JSON.parse(line)
        raise "histórico com lacuna na geração #{generation}" if revision["generation"] != generation

        digest.update(line)
        if previous && generation == previous["generation"]
          raise "prefixo histórico divergente" unless digest.hexdigest == previous["digest"]

          matched = true
        end
      end
      child.value
    end
    raise "exportação autenticada falhou" unless status.success?
    raise "histórico vazio" if generation.negative?
    raise "histórico truncado ou restaurado de cópia antiga" unless matched

    {"version" => VERSION, "generation" => generation, "digest" => digest.hexdigest}
  end

  def publish(value)
    parent = File.dirname(@anchor)
    Tempfile.create(".cerberus-anchor-", parent) do |file|
      file.write(JSON.generate(value) + "\n")
      file.flush
      file.fsync
      File.rename(file.path, @anchor)
      File.open(parent, "r", &:fsync)
    end
  end
end

if $PROGRAM_NAME == __FILE__
  begin
    raise "uso: witness.rb init|verify|advance ÂNCORA BANCO CHAVE" unless ARGV.size == 4

    mode, anchor, database, key = ARGV
    File.umask(0o077)
    puts JSON.generate(Witness.new(anchor).run(mode, database, key))
  rescue SystemCallError, JSON::ParserError, RuntimeError => error
    warn "Testemunha recusou a operação (#{error})"
    exit 1
  end
end
